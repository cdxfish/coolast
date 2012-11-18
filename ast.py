#!/usr/bin/env python
"""

"""

import sys
import os


from pprint import pprint

import astparse


######################################################################
# Simple Python AST
######################################################################

def make_simple_action_fn():
  return lambda r, p: [r] + p[1:]


simple_action_dict = {
  'program': make_simple_action_fn(),
  'class_list': make_simple_action_fn(),
  'class': make_simple_action_fn(),
  'simple_case': make_simple_action_fn(),
  'case_list': make_simple_action_fn(),
  'expr_list': make_simple_action_fn(),
  'actuals': make_simple_action_fn(),
  'expr_aux': make_simple_action_fn(),
  'expr': make_simple_action_fn(),
  'formal': make_simple_action_fn(),
  'formal_list': make_simple_action_fn(),
  'formals': make_simple_action_fn(),
  'feature': make_simple_action_fn(),
  'feature_list': make_simple_action_fn(),
  'optional_feature_list': make_simple_action_fn(),
}


######################################################################
# Dump out the Simple Python AST
# in the same format as the Cool AST (for testing)
######################################################################

def print_node(node, indent):
  if node[0] == 'expr':
    pad = ' ' * indent
    return '%s%s%s %s\n' % (print_node(node[1], indent + 1), pad, node[2], node[3])
  else:
    first = True
    out = ''
    for elm in node[1:]:
      if first and type(elm) is int:
        elm = '#%d' % elm

      if type(elm) in [list, tuple]:
        out += print_node(elm, indent + 1)
      else:
        out += '%s%s\n' % (' ' * indent, elm)
      first = False
    return out


def py_ast_to_cool_ast(ast):
  print '%s' % print_node(ast, 0)


######################################################################
# Rich AST
######################################################################

#
#
#
class AstNode(object):
  def __init__(self, name, children):
    pass

  def children(self):
    pass

  def recurse(self):
    pass


class Program(AstNode):
  def __init__(self, params):
    self.classes = params[1]


  constructor class_(name : Symbol; parent: Symbol; features : Features; filename : Symbol): Class_;
  constructor method(name : Symbol; formals : Formals; return_type : Symbol; expr: Expression) : Feature;
 constructor attr(name, type_decl : Symbol; init : Expression) : Feature;
  constructor formal(name, type_decl: Symbol) : Formal;
  constructor branch(name, type_decl: Symbol; expr: Expression): Case;
  constructor assign(name : Symbol; expr : Expression) : Expression;
  constructor static_dispatch(expr: Expression; type_name : Symbol; name : Symbol; actual : Expressions) : Expression;
  constructor dispatch(expr : Expression; name : Symbol; actual : Expressions) : Expression;
  constructor cond(pred, then_exp, else_exp : Expression): Expression;
  constructor loop(pred, body: Expression) : Expression;
  constructor typcase(expr: Expression; cases: Cases): Expression;
  constructor block(body: Expressions) : Expression;
  constructor let(identifier, type_decl: Symbol; init, body: Expression): Expression;
  constructor plus(e1, e2: Expression) : Expression;
  constructor  sub(e1, e2: Expression) : Expression;
  constructor  mul(e1, e2: Expression) : Expression;
  constructor divide(e1, e2: Expression) : Expression;
  constructor  neg(e1: Expression) : Expression;
  constructor   lt(e1, e2: Expression) : Expression;
  constructor   eq(e1, e2: Expression) : Expression;
  constructor  leq(e1, e2: Expression) : Expression;
  constructor comp(e1: Expression) : Expression;
  constructor int_const(token: Symbol) : Expression;
  constructor bool_const(val: Boolean) : Expression;
  constructor string_const(token: Symbol) : Expression;
  constructor new_(type_name: Symbol): Expression;
  constructor isvoid(e1: Expression): Expression;
  constructor no_expr(): Expression;
  constructor object(name: Symbol): Expression;


if __name__ == '__main__':
  # # Test my ast lexer
  # lexer = build_ast_lexer()

  # # Test the parser

  # # Open up stdin
  text = sys.stdin.read()
  # lexer.input(text)
  # for tok in lexer:
  #   print tok

  parser = astparse.build_ast_parser(simple_action_dict)
  result = parser.parse(text, lexer=astparse.build_ast_lexer())
  py_ast_to_cool_ast(result)



# What should the ast look like?
#
#
# classes with values?  named tuples?  dictionaries?  tuples?
#
# Traversals: BFS, DFS, a way to remember scopes for symbol tables, get children
#
#
#
#
#
