import unittest
from operator import not_

from xml.dom.minidom import parseString

from domxpath import Compile, Environment
from datamodel import any

def compose(a, b) :
  return lambda *i : a(b(*i))
  
none = compose(not_, any)
  
all = (lambda seq, pred=bool : none(seq, compose(not_, pred)))

test_doc = """<?xml version="1.0"?>
<level1>
 <level2 id="1">
 </level2>
 <level2 id="2">
   <level3>
   </level3>
 </level2>
 <level2 id="3">
   <level3>
     <level4>
     </level4>
   </level3>
 </level2>
</level1>
"""

class PredicatesTestSuite(unittest.TestCase) :
  
  def setUp(self) :
    self.test_doc = parseString(test_doc)
    #self.env = Environment()

  def test1(self) :
    expr = Compile("/level1/level2[level3]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 2)
    self.assert_(all(l, lambda n : n.tagName == "level2"))
    
  def test2(self) :
    expr = Compile("/level1/level2[level3/level4]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 1)
    self.assert_(all(l, lambda n : n.tagName == "level2"))
    
  def test3(self) :
    expr = Compile("/level1/level2[no_node]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 0)
    
  def test4(self) :
    expr = Compile("/level1/level2[1]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 1)
    self.assert_(l[0].getAttribute("id") == "1")
    
  def test5(self) :
    expr = Compile("/level1/level2[2]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 1)
    self.assert_(l[0].getAttribute("id") == "2")
    
  def test6(self) :
    expr = Compile("/level1/level2[3]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 1)
    self.assert_(l[0].getAttribute("id") == "3")
    
  def test7(self) :
    expr = Compile("/level1/level2[3][1]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 1)
    self.assert_(l[0].getAttribute("id") == "3")
    
  def test8(self) :
    expr = Compile("/level1/level2[3][2]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 0)
    
  def test9(self) :
    expr = Compile("/level1/level2[level3][1]")
    l = list(expr(self.test_doc, Environment()))
    self.assert_(len(l) == 1)
    self.assert_(all(l, lambda n : n.tagName == "level2"))
    
def suite() :
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(PredicatesTestSuite))
  return suite
  
if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())