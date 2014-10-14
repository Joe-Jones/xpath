#from unittest import TestCase
import unittest
from datamodel import aggregate, any
from operator import concat, add, eq

class SequenceTestSuite(unittest.TestCase) :

  def setUp(self) :
    self.stringList = ["a", "b", "c", "d"]
    self.numberList = [1, 2, 3, 4]
    
  def stringIterator(self) :
    for s in self.stringList :
      yield s
      
  def numberIterator(self) :
    for n in self.numberList :
      yield n
      
  def emptyIterator(self) :
    if False :
      yield None
    
  def testAggregate1(self) :
    self.assertEqual("abcd", aggregate(concat, "", self.stringList))
    
  def testAggregate2(self) :
    self.assertEqual("seedabcd", aggregate(concat, "seed", self.stringList))
    
  def testAggregate3(self) :
    self.assertEqual("abcd", aggregate(concat, "", self.stringIterator()))
    
  def testAggregate4(self) :
    self.assertEqual("seedabcd", aggregate(concat, "seed", self.stringIterator()))
    
  def testAggregate5(self) :
    self.assertEqual(10, aggregate(add, 0, self.numberList))
    
  def testAggregate6(self) :
    self.assertEqual(25, aggregate(add, 15, self.numberList))
    
  def testAggregate7(self) :
    self.assertEqual(10, aggregate(add, 0, self.numberIterator()))
    
  def testAggregate8(self) :
    self.assertEqual(25, aggregate(add, 15, self.numberIterator()))
    
  def testAggregate9(self) :
    self.assertEqual(10, aggregate(add, 10, []))
    
  def testAggregate9(self) :
    self.assertEqual(10, aggregate(add, 10, self.emptyIterator()))
    
  def testAny1(self) :
    self.assert_(any(self.stringList, lambda a: eq(a, "a")))
    
  def testAny2(self) :
    self.assert_(any(self.stringList, lambda a: eq(a, "b")))
    
  def testAny3(self) :
    self.assert_(any(self.stringList, lambda a: eq(a, "c")))
    
  def testAny4(self) :
    self.assert_(any(self.stringList, lambda a: eq(a, "d")))
    
  def testAny5(self) :
    self.assert_(not any(self.stringList, lambda a: eq(a, "x")))
    
  def testAny6(self) :
    self.assert_(any(self.stringIterator(), lambda a: eq(a, "a")))
    
  def testAny7(self) :
    self.assert_(any(self.stringIterator(), lambda a: eq(a, "b")))
    
  def testAny8(self) :
    self.assert_(any(self.stringIterator(), lambda a: eq(a, "c")))
    
  def testAny9(self) :
    self.assert_(any(self.stringIterator(), lambda a: eq(a, "d")))
    
  def testAny10(self) :
    self.assert_(not any(self.stringIterator(), lambda a: eq(a, "x")))
    
  def testAny11(self) :
    self.assert_(any(self.numberList, lambda a: eq(a, 1)))
    
  def testAny12(self) :
    self.assert_(any(self.numberList, lambda a: eq(a, 2)))
    
  def testAny13(self) :
    self.assert_(any(self.numberList, lambda a: eq(a, 3)))
    
  def testAny14(self) :
    self.assert_(any(self.numberList, lambda a: eq(a, 4)))
    
  def testAny15(self) :
    self.assert_(not any(self.numberList, lambda a: eq(a, 100)))
    
  def testAny16(self) :
    self.assert_(any(self.numberIterator(), lambda a: eq(a, 1)))
    
  def testAny17(self) :
    self.assert_(any(self.numberIterator(), lambda a: eq(a, 2)))
    
  def testAny18(self) :
    self.assert_(any(self.numberIterator(), lambda a: eq(a, 3)))
    
  def testAny19(self) :
    self.assert_(any(self.numberIterator(), lambda a: eq(a, 4)))
    
  def testAny20(self) :
    self.assert_(not any(self.numberIterator(), lambda a: eq(a, 100)))
    
  def testAny21(self) :
    self.assert_(not any(self.emptyIterator(), lambda a: eq(a, 100)))
    
  def testAny22(self) :
    self.assert_(not any(self.emptyIterator(), lambda a: eq(a, 100)))
    
def suite() :
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(SequenceTestSuite))
  return suite
  
if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
    
