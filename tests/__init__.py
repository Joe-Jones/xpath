import unittest
import datamodel_tests, path_tests, operators, function_tests
from domxpath import Compile, Environment
from itertools import chain
from xml.dom.minidom import parseString

class XPathTest(unittest.TestCase):

  def __init__(self, test_string, test_doc, result, description) :
    self.test_string = test_string
    self.test_doc = test_doc
    self.result = result
    self.description = description
    unittest.TestCase.__init__(self)
    
  def runTest(self) :
    if self.test_doc :
      self.test_doc = parseString(self.test_doc)
    expr = Compile(self.test_string)
    self.assert_(expr(self.test_doc, Environment()) == self.result)
    
  def shortDescription(self) :
    return self.description
    
  def createSuite(klass, test_list) :
    suite = unittest.TestSuite()
    for test in test_list :
      suite.addTest(klass(test[0], test[1], test[2],
                                 "\"" + test[0] + "\" == " + str(test[2])))
    return suite
    
  createSuite = classmethod(createSuite)
  
  def createSymmetryTests(klass, test_list) :
    suite = unittest.TestSuite()
    for test in test_list :
      test_string = test[0] + test[1] + test[2]
      suite.addTest(klass(test_string, test[3], test[4],
                                 "\"" + test_string + "\" == " + str(test[4])))
      test_string = test[2] + test[1] + test[0]
      suite.addTest(klass(test_string, test[3], test[4],
                                 "\"" + test_string + "\" == " + str(test[4])))
    return suite
    
  createSymmetryTests = classmethod(createSymmetryTests)

test_imps = []

#try:
#  from xml.dom.ext.reader import Sax2
  
#  class XPathTestPyXML(XPathTest) :
  
#    reader = Sax2.Reader().fromString
    
#    parser_imp = "PyXML"
    
#  test_imps.append(XPathTestPyXML)
#except:
#  pass
  
try:
  from xml.dom.minidom import parseString
  
  class XPathTestminidom(XPathTest) :
  
    def reader(self, str) :
      return parseString(str)
      
    parser_imp = "minidom"
    
  test_imps.append(XPathTestminidom)
except:
  pass
    
def suite(testImps) :
  return unittest.TestSuite(tuple(chain([datamodel_tests.suite()],
                                  *[[path_tests.suite(imp),
                                    operators.suite(imp),
                                    function_tests.suite(imp)]
                                   for imp in testImps])))
  
if __name__ == '__main__':
    

  unittest.TextTestRunner(verbosity=2).run(suite(test_imps))
