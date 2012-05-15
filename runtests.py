import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest
import glob

from pyvinil.test import test_vhd

suite = unittest.TestSuite()
test_file_strings = glob.glob('pyvinil/test/test_*.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]
for module in module_strings:
  module = module.replace("/",".")
  mod = __import__(module, globals(), locals(), ['suite'])
  suitefn = getattr(mod, 'suite')
  suite.addTest(suitefn())

unittest.TextTestRunner().run(suite)