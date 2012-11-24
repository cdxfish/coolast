#!/usr/bin/env python
"""

"""

import sys
import os

from collections import namedtuple
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


ASTNode = namedtuple("ASTNode", "type children lineno expr_type parse_label")

def make_ast_node(children_spec, label=None):
  def copy_child_spec(p):
    spec = children_spec[p[2]]
    if type(spec) == dict:
      return dict([key, p[index]] for key, index in spec.iteritems())
    else:
      return dict(zip(spec, p[3:]))

  return lambda r, p: ASTNode(type=p[2].lower()[1:],
                              children=copy_child_spec(p),
                              lineno=p[1],
                              expr_type=None,
                              parse_label=r)

# def make_list_node(label):
#   return lambda r, p: ASTNode(type=label,
#                               children=p[1:],
#                               lineno=None,
#                               expr_type=None,
#                               parse_label=r)
def make_list_node(label):
  return lambda r, p: p[1:]


tuple_action_dict = {
  'program': make_ast_node({'_program': ['class_list']}),
  'class_list': make_list_node('classes'),
  'class': make_ast_node({'_class': {'name': 3,
                                     'parent': 4,
                                     'filename': 5,
                                     'features': 7}}),
  'simple_case': make_ast_node({'_branch': {'name': 3,
                                            'type_decl': 4,
                                            'expr': 5}}),
  'case_list': make_list_node('cases'),
  'expr_list': make_list_node('exprs'),
  'actuals': make_list_node('exprs'),
  'expr_aux': make_ast_node({
      '_no_expr': [],
      '_object': ['ID'],
      '_bool': ['INT_CONST'],
      '_string': ['STR_CONST'],
      '_int': ['INT_CONST'],
      '_comp': ['expr'],
      '_leq': ['expr', 'expr'],
      '_eq': ['expr', 'expr'],
      '_lt': ['expr', 'expr'],
      '_neg': ['expr'],
      '_divide': ['expr', 'expr'],
      '_mul': ['expr', 'expr'],
      '_sub': ['expr', 'expr'],
      '_plus': ['expr', 'expr'],
      '_isvoid': ['expr'],
      '_new': ['ID'],
      '_typcase': ['expr', 'case_list'],
      '_let': ['ID', 'ID', 'expr', 'expr'],
      '_block': ['expr_list'],
      '_loop': ['expr', 'expr'],
      '_cond': ['expr', 'expr', 'expr'],
      '_dispatch': ['expr', 'ID', 'actuals'],
      '_static_dispatch': ['expr', 'ID', 'ID', 'actuals'],
      '_assign': ['ID', 'expr']
  }),
  'expr': lambda r,p: None,
  'formal': make_ast_node({'name': 3, 'type_decl': 4}),
  'formal_list': make_list_node('formals'),
  'formals': make_list_node('formals'),
  'feature': make_ast_node({'ATTR': ['name', 'type_decl', 'init'],
                            'METHOD': ['name', 'formals', 'return_type', 'expr']}),
  'feature_list': make_list_node('features'),
  'optional_feature_list': make_list_node('features'),
}


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


