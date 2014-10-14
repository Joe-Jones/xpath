import unittest

doc = """<?xml version="1.0"?>
<root>
  <one/>
  <one/>
  <one/>
  
  <two/>
  <two/>
</root>
"""

tests = [
    ["count(/root/one) = 3", doc, True],
    ["count(/root/two) = 2", doc, True],
    ["count(/root/one|/root/two) = 5", doc, True],

]
  
  
def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(XPathTest.createSuite(tests))
