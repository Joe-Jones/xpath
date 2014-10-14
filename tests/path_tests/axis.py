import unittest
  
doc = """<?xml version="1.0"?>
<root hi="there">
  <anItem hi="there">1</anItem>
  <anItem hi="there" now="again">2</anItem>
</root>"""

doc2 = """<?xml version="1.0"?><one><two>Three</two><two/></one>"""

tests = [
    ["count(/child::root)", doc, 1],
    ["count(/child::root/child::anItem) = 2", doc, True],
    [" count ( / child   :: root ) ", doc, 1],
    [" count ( / child :: root / child :: anItem ) = 2 ", doc, True],
    ["count(/child::*) = 1", doc, True],
    ["count(/child::*/child::*) = 2", doc, True],
    ["count(/descendant::anItem) = 2", doc, True],
    ["count(/descendant::*) = 3", doc, True],
    ["count(/descendant::pigs) = 0", doc, True],
    ["count(/root/attribute::hi) = 1", doc, True],
    ["count(/root/attribute::*) = 1", doc, True],
    ["count(/descendant::*/attribute::hi) = 3", doc, True],
    ["count(/descendant::*/attribute::*) = 4", doc, True],
    ["count(/descendant-or-self::node()) = 5", doc2, True],
    ["count(//*) = 3", doc2, True],
    ["count(/one//*) = 2", doc2, True],
    ["count(/one//.) = 4", doc2, True],
    ["local-name(/one/*/..) = 'one'", doc2, True],
]
  
  
def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(suite(XPathTest))

