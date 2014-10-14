import elements, predicates, axis, node_types
import unittest

def suite(testImp) :
  return unittest.TestSuite((
      elements.suite(),
      predicates.suite(),
      axis.suite(testImp),
      node_types.suite(testImp)))
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(suite(XPathTest))
