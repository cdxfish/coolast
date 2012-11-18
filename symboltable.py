"""
A Stack based symbol table for use with cool.

"""

from contextlib import contextmanager


class SymbolTable(object):
  """A simple Symbol Table implementation based on the normal cool compiler.

  This code supports defining symbols in different scope levels, and
  searching through enclosing scopes to find symbols that aren't defined
  in the current scope.

  """

  def __init__(self):
    self.scopes = [] # Get this from brownie
    self.enter_scope() # Add baby's first scope

  def current_scope(self):
    """Return the dictionary representing the current scope.

    This should primarily be used internally by `class`:SymbolTable,
    but it can be used externally if needed.

    """
    return self.scopes[-1]

  def add(self, symbol_name, data):
    """Add a symbol to the current scope.

    Note that this will fail if the symbol is already defined
    in the current scope.

    """
    if symbol_name in self.scopes[-1]:
      raise ValueError('Symbol %s already defined' % symbol_name)

    self.current_scope()[symbol_name] = data

  def remove(self, symbol_name):
    """Delete a symbol from the current scope.

    It will throw an exception if the symbol doesn't exist.

    """
    del self.current_scope()[symbol_name]

  def find(self, symbol_name):
    """Search the current scope and all enclosing scopes for symbol_name.

    Returns None if the symbol_name doesn't exist anywhere.

    """
    # Search backwards through the stack until we find the missing symbol
    for scope in reversed(self.scopes):
      if symbol_name in scope:
        return scope[symbol_name]

    return None

  def enter_scope(self):
    """Go into a new scope."""
    self.scopes.append({})

  def leave_scope(self):
    """Pop out of the current scope.

    Note that the current scope will be destroyed.

    """
    self.scopes.pop()

  def check_scope(self, symbol_name):
    """Does the symbol exist in the current scope only?

    Unlike find, this does not search through the enclosing scopes.

    """
    return self.current_scope().get(symbol_name, None)

  @contextmanager
  def in_scope(self):
    try:
      self.enter_scope()
      yield self
    finally:
      self.leave_scope()
