#!/usr/bin/env python
"""

"""

import sys
import os

from collections import namedtuple
from pprint import pprint

import astparse
import types

from brownie.datastructures import OrderedDict


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


# class ASTNode(object):
#   def __init__(self, rule, elements):
#     self.rule = rule
#     self.children = elements[1:]


# Want to traverse each one and leave meta data.
#
# step one
#  convert ast -> inheritance graph,
#  fail if ig is invalid.
#  -> no cycleso
#
#
# notes:
#  expressions need to be able to dump out their types
#  need to semantically traverse the tree (just recurse through everything)
#  be able to add type info
#
#
#


#ASTNode = namedtuple("ASTNode", "type elms lineno expr_type parse_label")
class ASTNode(object):
  def __init__(self, rule, rule_vals, rule_labels, type_index):
    self.rule = rule
    # XXX Is this a good name?
    self.rule_vals = {}

    if type_index is not None:
      self.type = rule_vals[type_index]
      active_labels = rule_labels[self.type]
    else:
      self.type = self.rule
      active_labels = rule_labels

    self.rule_vals = OrderedDict(zip((label.lower() for label in active_labels),
                                     rule_vals))

  @property
  def values(self):
    return self.rule_vals.values()

  @property
  def items(self):
    return self.rule_vals.items()

  def __getattr__(self, attr):
    if attr in self.__dict__:
      return self.__dict__[attr]

    if attr not in self.rule_vals:
      raise AttributeError('Unable to find %s' % attr)

    return self.rule_vals[attr]

  def set_val(self, name, val):
    self.rule_vals[name] = val


def make_ast_node(elms_spec, type_index=1):
  return lambda r, p: ASTNode(r, p[1:], elms_spec, type_index=type_index)


def make_list_node():
  return lambda r, p: p[1:]


def handle_list(r, p):
  if len(p) == 3:
    return p[1] + [p[2]]
  else:
    return [p[1]]


def handle_paren_list(r, p):
  if len(p) == 4:
    return p[2]
  else:
    return []


tuple_action_dict = {
  'program': make_ast_node({'_program': ['LINENO', 'PROGRAM', 'class_list']}),
  'class_list': make_list_node(),
  'class': make_ast_node({'_class': ['LINENO', 'CLASS', 'name', 'parent', 'filename', 'LPAREN', 'features', 'RPAREN']}),
  'simple_case': make_ast_node({'_branch': ['LINENO', 'BRANCH', 'name', 'type_decl', 'expr']}),
  'case_list': handle_list,
  'expr_list': handle_list,
  'actuals': handle_paren_list,
  'expr_aux': make_ast_node({
      '_no_expr': ['LINENO', 'NO_EXPR'],
      '_object': ['LINENO', 'OBJECT', 'ID'],
      '_bool': ['LINENO', 'BOOL', 'INT_CONST'],
      '_string': ['LINENO', 'STRING', 'STR_CONST'],
      '_int': ['LINENO', 'INT', 'INT_CONST'],
      '_comp': ['LINENO', 'COMP', 'expr'],
      '_leq': ['LINENO', 'LEQ', 'expr1', 'expr2'],
      '_eq': ['LINENO', 'EQ', 'expr1', 'expr2'],
      '_lt': ['LINENO', 'LT', 'expr1', 'expr2'],
      '_neg': ['LINENO', 'NEG', 'expr'],
      '_divide': ['LINENO', 'DIVIDE', 'expr1', 'expr2'],
      '_mul': ['LINENO', 'MUL', 'expr1', 'expr2'],
      '_sub': ['LINENO', 'SUB', 'expr1', 'expr2'],
      '_plus': ['LINENO', 'PLUS', 'expr1', 'expr2'],
      '_isvoid': ['LINENO', 'ISVOID', 'expr'],
      '_new': ['LINENO', 'NEW', 'ID'],
      '_typcase': ['LINENO', 'TYPCASE', 'expr', 'case_list'],
      '_let': ['LINENO', 'LET', 'ID1', 'ID2', 'expr1', 'expr2'],
      '_block': ['LINENO', 'BLOCK', 'expr_list'],
      '_loop': ['LINENO', 'LOOP', 'expr1', 'expr2'],
      '_cond': ['LINENO', 'COND', 'expr1', 'expr2', 'expr3'],
      '_dispatch': ['LINENO', 'DISPATCH', 'expr', 'func_name', 'actuals'],
      '_static_dispatch': ['LINENO', 'STATIC', 'expr', 'ID1', 'ID2', 'actuals'],
      '_assign': ['LINENO', 'ASSIGN', 'ID', 'expr']
  }),
  'expr': make_ast_node(['expr_aux', 'COLON', 'type'], type_index=None),
  'formal': make_ast_node(['LINENO', 'FORMAL', 'ID1', 'ID2']),
  'formal_list': handle_list,
  'formals': make_list_node(),
  'feature': make_ast_node({'_attr': ['LINENO', 'ATTR', 'name', 'type_decl', 'init'],
                            '_method': ['LINENO', 'METHOD', 'name', 'formals', 'return_type', 'expr']}),
  'feature_list': handle_list,
  'optional_feature_list': lambda r, p: p[1]
}


def ast_to_str(ast_node, indent=0):
  def recurse(e):
    return ast_to_str(e, indent + 1)

  if type(ast_node) in [list, tuple]:
    return ''.join(recurse(node) for node in ast_node)
  elif not ast_node or type(ast_node) != ASTNode:
    return ''
  else:
    if ast_node.type == 'expr':
      pad = ' ' * indent
      values = ast_node.values
      return '%s%s%s %s\n' % (recurse(values[0]), pad, values[1], values[2])
    else:
      pad = ' ' * indent
      def output_indent(elm):
        return '%s%s\n' % (pad, elm)

      out = ''
      for kind, val in ast_node.items:
        if kind in ['str_const', 'filename']:
          out += output_indent('\"%s\"' % val)
        elif kind == 'lineno':
          out += output_indent('#%d' % val)
        elif kind == 'actuals':
          out += output_indent('(\n%s%s)' % (recurse(val), pad))
        elif type(val) == ASTNode:
          out += recurse(val)
        elif type(val) in [list, tuple]:
          out += ''.join(recurse(v) for v in val)
        else:
          out += output_indent(val)

    return out



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
  def __init__(self, name, elms):
    pass

  def elms(self):
    pass

  def recurse(self):
    pass


class Program(AstNode):
  def __init__(self, params):
    self.classes = params[1]


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

# def make_simple_action_fn():
#   return lambda r, p: [r] + p[1:]


# simple_action_dict = {
#   'program': make_simple_action_fn(),
#   'class_list': make_simple_action_fn(),
#   'class': make_simple_action_fn(),
#   'simple_case': make_simple_action_fn(),
#   'case_list': make_simple_action_fn(),
#   'expr_list': make_simple_action_fn(),
#   'actuals': make_simple_action_fn(),
#   'expr_aux': make_simple_action_fn(),
#   'expr': make_simple_action_fn(),
#   'formal': make_simple_action_fn(),
#   'formal_list': make_simple_action_fn(),
#   'formals': make_simple_action_fn(),
#   'feature': make_simple_action_fn(),
#   'feature_list': make_simple_action_fn(),
#   'optional_feature_list': make_simple_action_fn(),
# }


# def print_node(node, indent):
#   if node[0] == 'expr':
#     pad = ' ' * indent
#     return '%s%s%s %s\n' % (print_node(node[1], indent + 1), pad, node[2], node[3])
#   else:
#     first = True
#     out = ''
#     for elm in node[1:]:
#       if first and type(elm) is int:
#         elm = '#%d' % elm

#       if type(elm) in [list, tuple]:
#         out += print_node(elm, indent + 1)
#       else:
#         out += '%s%s\n' % (' ' * indent, elm)
#       first = False
#     return out


# def py_ast_to_cool_ast(ast):
#   print '%s' % print_node(ast, 0)


# if __name__ == '__main__':
#   # # Test my ast lexer
#   # lexer = build_ast_lexer()

#   # # Test the parser

#   # # Open up stdin
#   text = sys.stdin.read()
#   # lexer.input(text)
#   # for tok in lexer:
#   #   print tok

#   parser = build_ast_parser(simple_action_dict)
#   result = parser.parse(text, lexer=build_ast_lexer())
#   # pprint(result)
#   py_ast_to_cool_ast(result)



# What should the ast look like?
#
#
# classes with values?  named tuples?  dictionaries?  tuples?
#
# Traversals: BFS, DFS, a way to remember scopes for symbol tables, get children
#
#


