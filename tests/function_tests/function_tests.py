import unittest
  
doc = """<?xml version="1.0"?>
<root>
  <anItem>1</anItem>
  <anItem>2</anItem>
</root>"""

tests = [
    ["true ()", None, True],
    ["false()", None, False],
    ["/root/anItem[position()=1] = 2", doc, False],
    [" / root / anItem [ position()=1]=2", doc, False],
    [" / root / anItem [ position ( ) = 1 ] = 2 ", doc, False],
    ["boolean(true())", None, True],
    ["boolean(false())", None, False],
    ["boolean('')", None, False],
    ["boolean('Hi there')", None, True],
    ["boolean(/root/anItem)", doc, True],
    ["boolean(/root/anotherIten)", doc, False],
    [" boolean ( / root / anItem ) ", doc, True],
    [" boolean ( / root / anotherIten ) ", doc, False],
    ["boolean(1)", None, True],
    ["boolean(0)", None, False],
    ["concat('Hi there')", None, "Hi there"],
    ["concat('Hi there ', 'again')", None, "Hi there again"],
    ["concat('Hi there ', 'again ', 1)", None, "Hi there again 1"],
    ["concat('Hi there ', 'again ', /root/anItem[1])", doc, "Hi there again 1"],
    ["concat('Hi there ', 'again ', /root/anItem[2])", doc, "Hi there again 2"],
    ["concat('Hi there ', 'again ', /root/anItem)", doc, "Hi there again 1"],
    ["contains('Hi There', 'Hi')", None, True],
    ["contains('Hi There', 'There')", None, True],
    ["contains('Hi There', 'Not')", None, False],
    ["contains('Hi There', 1)", None, False],
    ["count(/)", doc, 1.0],
    ["count(/root)", doc, 1.0],
    ["count(/root/anItem)", doc, 2.0],
    ["count(/root/anItem[1])", doc, 1.0],
    ["number('4') = 4", None, True],
    ["number(true()) = 1", None, True],
    ["number(false()) = 0", None, True],
    ["number(/root/anItem[1]) = 1", doc, True],
    ["number(/root/anItem[2]) = 2", doc, True],
    ["number(/root/anItem[number() = 1]) = 1", doc, True],
    ["number(/root/anItem[number() = 2]) = 2", doc, True],
    ["string(17) = '17'", None, True],
    ["string(true()) = 'true'", None, True],
    ["string(false()) = 'false'", None, True],
    ["string(/root/anItem) = '1'", doc, True],
    ["string(/root/anItem[1]) = '1'", doc, True],
    ["string(/root/anItem[2]) = '2'", doc, True],
    ["number(/root/anItem[position() = last()]) = 2", doc, True],
    ["not(true())", None, False],
    ["not(false())", None, True],
    ["string-length('1234567890') = 10", None, True],
    ["string-length('12345') = 5", None, True],
    ["string-length('') = 0", None, True],
    ["string-length(/root/anItem) = 1", doc, True],
    ["round(1.23456) = 1", None, True],
    ["round(789.6464) = 790", None, True],
    ["local-name(/root) = 'root'", doc, True],
    
]
  
  
def suite(testImp) :
  return testImp.createSuite(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(suite(XPathTest))
