import unittest

test_doc = """<?xml version="1.0"?>
<root>
  <one>
    <node>a</node>
    <node>b</node>
    <node>c</node>
    <node>d</node>
  </one>
  <two>
    <node>q</node>
    <node>w</node>
    <node>e</node>
    <node>r</node>
    <node>t</node>
  </two>
  <three>
    <node>q</node>
    <node>w</node>
    <node>a</node>
    <node>r</node>
    <node>t</node>
  </three>
  <four>
    <node>c</node>
  </four>
  <four-and-a-bit>
    <node>c</node>
  </four-and-a-bit>
  <five>
    <node>x</node>
  </five>
  <six>
    <node>1</node>
    <node>2</node>
    <node>3</node>
    <node>4</node>
    <node>5</node>
  </six>
  <seven>
    <node>6</node>
    <node>7</node>
    <node>8</node>
    <node>9</node>
    <node>10</node>
  </seven>
  <eight>
    <node>6</node>
    <node>7</node>
    <node>not a number</node>
    <node>9</node>
    <node>10</node>
  </eight>
  <nine>
    <node>4</node>
  </nine>

</root>
"""

tests = [
    ["0", "=", "0", None, True],
    ["100", "=", "100", None, True],
    ["1.2345", "=", "1.2345", None, True],
    ["100", "=", "0", None, False],
    ["/root/one/node", "=", "/root/two/node", test_doc, False],
    ["/root/one/node", "=", "/root/three/node", test_doc, True],
    ["/root/one/node", "=", "/root/four/node", test_doc, True],
    ["/root/one/node", "=", "/root/five/node", test_doc, False],
    ["/root/four/node", "=", "/root/four-and-a-bit/node", test_doc, True],
    ["1", "=", "/root/six/node", test_doc, True],
    ["3", "=", "/root/six/node", test_doc, True],
    ["5", "=", "/root/six/node", test_doc, True],
    ["6", "=", "/root/six/node", test_doc, False],
    ["6", "=", "/root/eight/node", test_doc, True],
    ["1", "!=", "2", None, True],
    ["1", "!=", "1", None, False]
]
  
  
def suite(testImp) :
  return testImp.createSymmetryTests(tests)
  
if __name__ == '__main__':
  from tests import XPathTest
  unittest.TextTestRunner(verbosity=2).run(XPathTest.createSymmetryTests(tests))
