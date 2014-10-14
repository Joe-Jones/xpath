import unittest

doc = """<?xml version="1.0"?>
<root>
  <anItem><!--A comment--></anItem>
  <anItem>This is some text</anItem>
  <anItem>This is some more test</anItem>
</root>"""

tests = [
    ["string(/root/anItem/comment()) = 'A comment'", doc, True],    
    ["string(/child::root/child::anItem/child::comment()) = 'A comment'", doc, True], 
    ["string(/child::root/child::anItem/child::comment()) = 'A comment xxx'", doc, False],
    ["string(/root/anItem[2]/text()) = 'This is some text'", doc, True],
    ["string(/root/anItem[2]/text()) = 'This is some text xx'", doc, False],
]
  
def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(suite(XPathTest))
