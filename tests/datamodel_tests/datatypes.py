import unittest
from itertools import izip
from xml.dom.minidom import parseString
from datamodel import unPack, allDescendants, any, isaSequence, boolean

def makeIter(v) :
  yield v
  
def emptyIter() :
  if False :
    yield 1
  
def sequencesEqual(s1,s2) :
  return not any(izip(s1,s2), lambda pair: pair[0] != pair[1])
  
test_doc1 = """<?xml version="1.0"?>
<one id="1">
  <two id="2">&lt;
    <three id="3"/>
    <!--Hi-->
    <four id="4"/>
    <?ssl is there?>
    <![CDATA[This text is in a CDATA Section]]>
    <five id="5" hiei="123123">
      <six id="6"/>
    </five>
  </two>
</one>
"""

class DataTypesTestSuite(unittest.TestCase) :

  def setUp(self) :
    self.test_doc1 = parseString(test_doc1)
    
  def testUnpack1(self) :
    self.assert_(unPack("xxx") == "xxx")
    
  def testUnpack2(self) :
    self.assert_(unPack(u"xxx") == u"xxx")
    
  def testUnpack3(self) :
    self.assert_(unPack(float(3.555)) == float(3.555))
    
  def testUnpack4(self) :
    self.assert_(unPack(True) == True)
    
  def testUnpack5(self) :
    self.assert_(unPack(["xxx"]) == "xxx")
    
  def testUnpack6(self) :
    self.assert_(unPack([u"xxx"]) == u"xxx")
    
  def testUnpack7(self) :
    self.assert_(unPack([float(3.555)]) == float(3.555))
    
  def testUnpack8(self) :
    self.assert_(unPack([True]) == True)
    
  def testUnpack9(self) :
    self.assert_(unPack(makeIter("xxx")) == "xxx")
    
  def testUnpack10(self) :
    self.assert_(unPack(makeIter(u"xxx")) == u"xxx")
    
  def testUnpack11(self) :
    self.assert_(unPack(makeIter(float(3.555))) == float(3.555))
    
  def testUnpack12(self) :
    self.assert_(unPack(makeIter(True)) == True)
    
  def testUnpack13(self) :
    self.assert_(
        sequencesEqual(
            unPack(allDescendants(self.test_doc1)),
            allDescendants(self.test_doc1)))
    
  def testUnpack14(self) :
    self.assert_(list(unPack([])) == [])
    
  def testUnpack15(self) :
    self.assert_(list(unPack(emptyIter())) == [])
    
  def testisaSequence1(self) :
    self.assert_(isaSequence([]))
    
  def testisaSequence2(self) :
    self.assert_(not isaSequence(1))
    
  #def testunPackAndCast1(self) :
  #  var = iter([1])
  
  def testboolean1(self) :
    self.assert_(not boolean(float(0)))
    
  def testboolean2(self) :
    self.assert_(boolean(float(1)))
    
  def testboolean3(self) :
    self.assert_(boolean(float(123.5623)))
    
  def testboolean4(self) :
    self.assert_(not boolean([float(0)]))
    
  def testboolean5(self) :
    self.assert_(boolean([float(1)]))
    
  def testboolean6(self) :
    self.assert_(boolean([float(123.5623)]))
    
  def testboolean7(self) :
    self.assert_(not boolean(iter([float(0)])))
    
  def testboolean8(self) :
    self.assert_(boolean(iter([float(1)])))
    
  def testboolean9(self) :
    self.assert_(boolean(iter([float(123.5623)])))
    
  def testboolean10(self) :
    self.assert_(not boolean(False))
    
  def testboolean11(self) :
    self.assert_(boolean(True))
    
  def testboolean12(self) :
    self.assert_(not boolean([False]))
    
  def testboolean13(self) :
    self.assert_(boolean([True]))
    
  def testboolean14(self) :
    self.assert_(not boolean(iter([False])))
    
  def testboolean15(self) :
    self.assert_(boolean(iter([True])))
    
  def testboolean16(self) :
    self.assert_(not boolean(""))
    
  def testboolean17(self) :
    self.assert_(boolean("a string"))
    
  def testboolean18(self) :
    self.assert_(not boolean([""]))
    
  def testboolean19(self) :
    self.assert_(boolean(["a string"]))
    
  def testboolean20(self) :
    self.assert_(not boolean(iter([""])))
    
  def testboolean21(self) :
    self.assert_(boolean(iter(["a string"])))
    
  def testboolean22(self) :
    self.assert_(not boolean(self.test_doc1.getElementsByTagName("notag")))
    
  def testboolean23(self) :
    self.assert_(boolean(self.test_doc1.getElementsByTagName("four")))
    
  def testboolean24(self) :
    self.assert_(not boolean(list(self.test_doc1.getElementsByTagName("notag"))))
    
  def testboolean25(self) :
    self.assert_(boolean(list(self.test_doc1.getElementsByTagName("four"))))
    
  def testboolean26(self) :
    self.assert_(not boolean(iter(list(self.test_doc1.getElementsByTagName("notag")))))
    
  def testboolean27(self) :
    self.assert_(boolean(iter(list(self.test_doc1.getElementsByTagName("four")))))
    
  def testUnPackThenBoolena1(self) :
    self.assert_(not boolean(unPack(self.test_doc1.getElementsByTagName("notag"))))
    
  def testUnPackThenBoolena2(self) :
    self.assert_(boolean(unPack(self.test_doc1.getElementsByTagName("four"))))
    
  def testUnPackThenBoolena3(self) :
    self.assert_(not boolean(unPack(list(self.test_doc1.getElementsByTagName("notag")))))
    
  def testUnPackThenBoolena4(self) :
    self.assert_(boolean(unPack(list(self.test_doc1.getElementsByTagName("four")))))
    
  def testUnPackThenBoolena5(self) :
    self.assert_(not boolean(unPack(iter(list(self.test_doc1.getElementsByTagName("notag"))))))
    
  def testUnPackThenBoolena6(self) :
    self.assert_(boolean(unPack(iter(list(self.test_doc1.getElementsByTagName("four"))))))
    
  def testUnPackThenBoolena7(self) :
    self.assert_(not boolean(unPack(float(0))))
    
  def testUnPackThenBoolena8(self) :
    self.assert_(boolean(unPack(float(1))))
    
  def testUnPackThenBoolena9(self) :
    self.assert_(boolean(unPack(float(123.5623))))
    
  def testUnPackThenBoolena10(self) :
    self.assert_(not boolean(unPack([float(0)])))
    
  def testUnPackThenBoolena11(self) :
    self.assert_(boolean(unPack([float(1)])))
    
  def testUnPackThenBoolena12(self) :
    self.assert_(boolean(unPack([float(123.5623)])))
    
  def testUnPackThenBoolena13(self) :
    self.assert_(not boolean(unPack(iter([float(0)]))))
    
  def testUnPackThenBoolena14(self) :
    self.assert_(boolean(unPack(iter([float(1)]))))
    
  def testUnPackThenBoolena15(self) :
    self.assert_(boolean(unPack(iter([float(123.5623)]))))
    
  def testUnPackThenBoolena16(self) :
    self.assert_(not boolean(unPack("")))
    
  def testUnPackThenBoolena17(self) :
    self.assert_(boolean(unPack("a string")))
    
  def testUnPackThenBoolena18(self) :
    self.assert_(not boolean(unPack([""])))
    
  def testUnPackThenBoolena19(self) :
    self.assert_(boolean(unPack(["a string"])))
    
  def testUnPackThenBoolena20(self) :
    self.assert_(not boolean(unPack(iter([""]))))
    
  def testUnPackThenBoolena21(self) :
    self.assert_(boolean(unPack(iter(["a string"]))))
    
    
    
def suite() :
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(DataTypesTestSuite))
  return suite
  
if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
