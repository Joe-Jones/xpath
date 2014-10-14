import unittest
from xml.dom.minidom import parseString
from domxpath import Compile, Environment

test_doc = u"""<?xml version="1.0"?>
<one>
  <two/>
  <two>
    <three/>
  </two>
  <two>
    <three/>
    <three/>
  </two>
</one>
"""

test_doc_ns = u"""<?xml version="1.0"?>
<one xmlns="http://blablabla/a_namepace">
  <two/>
  <sss:two xmlns:sss="http://sss.org///?sss">
    <three/>
    <sss:three/>
  </sss:two>
  <two>
    <three/>
  </two>
</one>
"""

class ElementsTestSuite(unittest.TestCase) :

  def setUp(self) : 
    self.test_doc = parseString(test_doc)
    self.test_doc_ns = parseString(test_doc_ns)
    self.env = Environment(nsMap = { "bla" : "http://blablabla/a_namepace",
                                     "s"   : "http://sss.org///?sss"})

  def test1(self) :
    expr = Compile("/")
    l = expr(self.test_doc, Environment())
    root = l.next()
    self.assert_(root == self.test_doc)
    
  def test2(self) :
    expr = Compile("/*")
    l = expr(self.test_doc, Environment())
    root = l.next()
    self.assert_(root == self.test_doc.documentElement)
    
  def test3(self) :
    expr = Compile("/one")
    l = expr(self.test_doc, Environment())
    root = l.next()
    self.assert_(root == self.test_doc.documentElement)
    
  def test4(self) :
    expr = Compile("/one/two")
    l = expr(self.test_doc, Environment())
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "two")
    self.assert_(count == 3)
    
  def test5(self) :
    expr = Compile("/one/*")
    l = expr(self.test_doc, Environment())
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "two")
    self.assert_(count == 3)
    
  def test6(self) :
    expr = Compile("/one/two/three")
    l = expr(self.test_doc, Environment())
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "three")
    self.assert_(count == 3)
    
  def test7(self) :
    expr = Compile("/one/two/*")
    l = expr(self.test_doc, Environment())
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "three")
    self.assert_(count == 3)
    
  def test8(self) :
    expr = Compile("/bla:one")
    l = expr(self.test_doc_ns, self.env)
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "one")
    self.assert_(count == 1)
    
  def test9(self) :
    expr = Compile("/one")
    l = expr(self.test_doc_ns, self.env)
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "one")
    self.assert_(count == 1)
    
  def test10(self) :
    expr = Compile("/*")
    l = expr(self.test_doc_ns, self.env)
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "one")
    self.assert_(count == 1)
    
  def test11(self) :
    expr = Compile("/one/two")
    l = expr(self.test_doc_ns, self.env)
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "two")
    self.assert_(count == 2)
    
  def test12(self) :
    expr = Compile("/one/bla:two")
    l = expr(self.test_doc_ns, self.env)
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "two")
    self.assert_(count == 2)
    
  def test13(self) :
    expr = Compile("/one/s:two")
    l = expr(self.test_doc_ns, self.env)
    count = 0
    for n in l :
      count += 1
      self.assert_(n.tagName == "sss:two")
    self.assert_(count == 1)
    
def suite() :
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(ElementsTestSuite))
  return suite
  
if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
