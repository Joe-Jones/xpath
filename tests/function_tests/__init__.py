import function_tests
import unittest

def suite(testImp) :
  return unittest.TestSuite((function_tests.suite(testImp),))
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(suite(XPathTest))
