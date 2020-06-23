from distutils.core import setup, Extension

setup(name='lcs', version='1.0', ext_modules=[Extension('lcs', ['lcs/module.c'])])