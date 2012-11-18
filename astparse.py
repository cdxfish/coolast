#!/usr/bin/env python
"""Provide a lexer and parser for the Stanford Cool compiler's AST output.

This module allows the user to use Python instead of Java or C++ as a
backend stage for the Cool compiler.  It can replace the semantic
analysis phase or the code generation phase.

"""

import sys
import os

import ply.lex as lex
import ply.yacc as yacc

from pprint import pprint

######################################################################
# Global variables
######################################################################

# Shared between the lexer and parser.
tokens = (
  'ASSIGN',
  'ATTR',
  'BLOCK',
  'BOOL',
  'BRANCH',
  'CLASS',
  'COLON',
  'COMP',
  'COND',
  'DISPATCH',
  'DIVIDE',
  'EQ',
  'FORMAL',
  'ISVOID',
  'LEQ',
  'LET',
  'LOOP',
  'LPAREN',
  'LT',
  'METHOD',
  'MUL',
  'NEG',
  'NEW',
  'NO_EXPR',
  'NO_TYPE',
  'OBJECT',
  'PLUS',
  'PROGRAM',
  'RPAREN',
  'STATIC_DISPATCH',
  'STR',
  'SUB',
  'TYPCASE',
  'INT',
  'LINENO',
  'STR_CONST',
  'INT_CONST',
  'ID',
  )


######################################################################
# Lexer code.
######################################################################

def build_ast_lexer():

  # punctuation
  t_COLON = r':'
  t_LPAREN = r'\('
  t_RPAREN = r'\)'

  reserved_words = {
    '_assign': 'ASSIGN',
    '_attr': 'ATTR',
    '_block': 'BLOCK',
    '_bool': 'BOOL',
    '_branch': 'BRANCH',
    '_class': 'CLASS',
    '_comp': 'COMP',
    '_cond': 'COND',
    '_dispatch': 'DISPATCH',
    '_divide': 'DIVIDE',
    '_eq': 'EQ',
    '_formal': 'FORMAL',
    '_int': 'INT',
    '_isvoid': 'ISVOID',
    '_leq': 'LEQ',
    '_let': 'LET',
    '_loop': 'LOOP',
    '_lt': 'LT',
    '_method': 'METHOD',
    '_mul': 'MUL',
    '_neg': 'NEG',
    '_new': 'NEW',
    '_no_expr': 'NO_EXPR',
    '_no_type': 'NO_TYPE',
    '_object': 'OBJECT',
    '_plus': 'PLUS',
    '_program': 'PROGRAM',
    '_static_dispatch': 'STATIC_DISPATCH',
    '_string': 'STR',
    '_sub': 'SUB',
    '_typcase': 'TYPCASE',
  }

  def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  # Not sure I need a function
  def t_INT_CONST(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

  def t_LINENO(t):
    r'\#[0-9]+'
    t.value = int(t.value[1:])
    return t

  def t_ID(t):
    r'[a-zA-Z0-9_]+'
    t.type = reserved_words.get(t.value, 'ID')
    return t

  states = (
    ('STRING', 'exclusive'),
  )
  def t_STR_CONST(t):
    r'\"'
    t.lexer.begin('STRING')

  def t_STRING_escape_chars(t):
    r'\\(.|\n)'
    lexer.string_builder += {
      'b': '\b',
      't': '\t',
      'n': '\n',
      'f': '\f',
    }[t.value[1]]

  def t_STRING_end_quote(t):
    r'\"'
    t.lexer.begin('INITIAL')
    t.type = 'STR_CONST'
    t.value = lexer.string_builder
    lexer.string_builder = ''
    return t

  def t_STRING_any_char(t):
    r'.'
    lexer.string_builder += t.value

  t_STRING_ignore = ''
  def t_STRING_error(t):
    print 'ran into error char: %s' % t.value[0]
    sys.exit(1)

  t_ignore = ' \t\r'

  def t_error(t):
    print 'ran into error char: %s' % t.value[0]
    sys.exit(1)

  # Make the lexer in the function's environment
  lexer = lex.lex()

  # Add any state variables needed
  lexer.string_builder = ''

  return lexer


######################################################################
# Parser Code
######################################################################

def build_ast_parser(action_dict):
  def p_program(p):
    """program : LINENO PROGRAM class_list
               |
    """
    rule = 'program'
    p[0] = action_dict[rule](rule, p)

  def p_class_list(p):
    """class_list : class_list class
                  | class
    """
    rule = 'class_list'
    p[0] = action_dict[rule](rule, p)

  def p_class(p):
    "class : LINENO CLASS ID ID STR_CONST LPAREN optional_feature_list RPAREN"
    rule = 'class'
    p[0] = action_dict[rule](rule, p)

  def p_simple_case(p):
    "simple_case : LINENO BRANCH ID ID expr"
    rule = 'simple_case'
    p[0] = action_dict[rule](rule, p)

  def p_case_list(p):
    """case_list : case_list simple_case
                 | simple_case

    """
    rule = 'case_list'
    p[0] = action_dict[rule](rule, p)

  def p_expr_list(p):
    """expr_list : expr_list expr
                 | expr
    """
    rule = 'expr_list'
    p[0] = action_dict[rule](rule, p)

  def p_actuals(p):
    """actuals : LPAREN expr_list RPAREN
               | LPAREN RPAREN
    """
    rule = 'actuals'
    p[0] = action_dict[rule](rule, p)

  def p_expr_aux(p):
    """expr_aux : LINENO NO_EXPR
                | LINENO OBJECT ID
                | LINENO BOOL INT_CONST
                | LINENO STR STR_CONST
                | LINENO INT INT_CONST
                | LINENO COMP expr
                | LINENO LEQ expr expr
                | LINENO EQ expr expr
                | LINENO LT expr expr
                | LINENO NEG expr
                | LINENO DIVIDE expr expr
                | LINENO MUL expr expr
                | LINENO SUB expr expr
                | LINENO PLUS expr expr
                | LINENO ISVOID expr
                | LINENO NEW ID
                | LINENO TYPCASE expr case_list
                | LINENO LET ID ID expr expr
                | LINENO BLOCK expr_list
                | LINENO LOOP expr expr
                | LINENO COND expr expr expr
                | LINENO DISPATCH expr ID actuals
                | LINENO STATIC_DISPATCH expr ID ID actuals
                | LINENO ASSIGN ID expr
    """
    rule = 'expr_aux'
    p[0] = action_dict[rule](rule, p)

  def p_expr(p):
    """expr : expr_aux COLON NO_TYPE
            | expr_aux COLON ID
    """
    rule = 'expr'
    p[0] = action_dict[rule](rule, p)

  def p_formal(p):
    "formal : LINENO FORMAL ID ID"
    rule = 'formal'
    p[0] = action_dict[rule](rule, p)

  def p_formal_list(p):
    """formal_list : formal_list formal
                   | formal
    """
    rule = 'formal_list'
    p[0] = action_dict[rule](rule, p)

  def p_formals(p):
    """formals : formal_list
               |
    """
    rule = 'formals'
    p[0] = action_dict[rule](rule, p)

  def p_feature(p):
    """feature : LINENO ATTR ID ID expr
               | LINENO METHOD ID formals ID expr
    """
    rule = 'feature'
    p[0] = action_dict[rule](rule, p)

  def p_feature_list(p):
    """feature_list : feature_list feature
                    | feature
    """
    rule = 'feature_list'
    p[0] = action_dict[rule](rule, p)

  def p_optional_feature_list(p):
    """optional_feature_list : feature_list
                             |
    """
    rule = 'optional_feature_list'
    p[0] = action_dict[rule](rule, p)

  def p_error(p):
    print "Syntax error in input!: %s" % p

  return yacc.yacc()
