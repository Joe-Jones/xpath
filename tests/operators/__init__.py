import equality, relational, arithmetic, boolean, union
import unittest

def suite(testImp) :
  return unittest.TestSuite((
      equality.suite(testImp),
      relational.suite(testImp),
      arithmetic.suite(testImp),
      boolean.suite(testImp),
      union.suite(testImp)))
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(suite(XPathTest))
