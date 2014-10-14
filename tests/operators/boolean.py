import unittest

tests = [
    ["true() and true()", None, True],
    ["true() and false()", None, False],
    ["false() and true()", None, False],
    ["false() and false()", None, False],
    ["true() or true()", None, True],
    ["true() or false()", None, True],
    ["false() or true()", None, True],
    ["false() or false()", None, False],

]
  

def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(XPathTest.createSuite(tests))
