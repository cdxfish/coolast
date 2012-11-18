from nose.tools import eq_, assert_raises

from symboltable import SymbolTable

def test_simple():
  st = SymbolTable()

  val = 1
  st.add('a', val)
  eq_(st.find('a'), val)

  st.enter_scope()
  eq_(st.find('a'), val)

  st.leave_scope()
  eq_(st.find('a'), val)


def test_check_all_functions():
  st = SymbolTable()

  foo = [1,2,3]
  bar = 'hi'

  st.add('a', foo)
  st.add('b', bar)
  eq_(st.find('a'), foo)
  eq_(st.find('b'), bar)

  st.remove('a')
  assert not st.find('a')
  assert not st.check_scope('a')
  eq_(st.check_scope('b'), bar)

  st.add('c', foo)

  # with st.in_scope():
  #   assert st.find('c') == foo
  #   assert st.find('b') == bar
  #   assert not st.check_scope('c')
  #   assert not st.check_scope('b')
  #   st.add('b', foo)
  #   assert st.find('b') == foo

  eq_(st.find('b'), bar)


def test_check_scoping():
  st = SymbolTable()

  for val in xrange(0, 10):
    st.enter_scope()
    st.add('a', val)

  for val in xrange(9, -1, -1):
    assert st.find('a') == val
    st.leave_scope()
