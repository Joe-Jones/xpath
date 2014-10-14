import unittest

tests = [
    ["1+2", None, 3],
    ["5+45", None, 50],
    ["1+2+3+4+5+6", None, 21],
    [" 1 + 2 + 3 + 4 + 5 + 6 ", None, 21],
    ["5*5", None, 25],
    [" 2 + 5 * 3", None, 17],
    ["1 div 2", None, 0.5],
    ["1div2", None, 0.5],
    ["1 * 2 div 2", None, 1],
    [" (2 + 5) * 3", None, 21],
    [" - 1", None, -1],
    ["-1", None, -1],
    ["1 + -1", None, 0],
    [" 1 + - 1 ", None, 0],
    #["", None, True]#,
]
  
def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(XPathTest.createSuite(tests))
