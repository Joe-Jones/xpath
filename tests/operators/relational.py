import unittest

tests = [
    ["0<1", None, True],
    ["0>1", None, False],
    ["100>10", None, True],
    ["100<10", None, False],
    ["1.2345<=1.2345", None, True],
    ["100>=0", None, True],
    ["100<=0", None, False]#,
    #["/root/one/node", "=", "/root/two/node", test_doc, False],
    #["/root/one/node", "=", "/root/three/node", test_doc, True],
    #["/root/one/node", "=", "/root/four/node", test_doc, True],
    #["/root/one/node", "=", "/root/five/node", test_doc, False],
    #["/root/four/node", "=", "/root/four-and-a-bit/node", test_doc, True],
    #["1", "=", "/root/six/node", test_doc, True],
    #["3", "=", "/root/six/node", test_doc, True],
    #["5", "=", "/root/six/node", test_doc, True],
    #["6", "=", "/root/six/node", test_doc, False],
    #["6", "=", "/root/eight/node", test_doc, True],
    #["1", "!=", "2", None, True],
    #["1", "!=", "1", None, False]
]
  
  
def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(XPathTest.createSuite(tests))
