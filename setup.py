import setuptools

setuptools.setup(
  name = 'coolast',
  version = '0.1',
  license = 'BSD',
  description = open('README.txt').read(),
  author = 'Michael Scheinholtz',
  author_email = 'mike@cronus.ws',
  url = 'http://github.com/mschein/coolast',
  platforms = 'any',

  py_modules = ['symboltable', 'astparse', 'ast'],

  zip_safe = True,
  verbose = False,
)
