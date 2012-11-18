"""
A Stack based symbol table for use with cool.

"""

class SymbolTable(object):
  def __init__(self):
    """
    """
    self.scopes = [] # Get this from brownie
    self.enter_scope() # Add baby's first scope

  def current_scope(self):
    return self.scopes[-1]

  def add(self, symbol_name, data):
    # XXX What if it exists?
    if symbol_name in self.scopes[-1]:
      raise ValueError('Symbol %s already defined' % symbol_name)

    self.current_scope()[symbol_name] = data

  def remove(self, symbol_name):
    del self.current_scope()[symbol_name]

  def find(self, symbol_name):
    # Search backwards through the stack until we find the missing symbol
    for scope in reversed(self.scopes):
      if symbol_name in scope:
        return scope[symbol_name]

    return None

  def enter_scope(self):
    self.scopes.append({})

  def leave_scope(self):
    self.scopes.pop()

  def check_scope(self, symbol_name):
    return self.current_scope().get(symbol_name, None)

  # Make a decorator to do this.
  def in_scope(self):
    try:
      self.enter_scope()
      yield self.current_scope()
    finally:
      self.leave_scope()
