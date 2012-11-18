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

  py_modules = ['coolast'],

  zip_safe = True,
  verbose = False,
)
