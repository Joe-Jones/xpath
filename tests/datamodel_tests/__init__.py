import sequence, domnodes, datatypes
import unittest

def suite() :
  return unittest.TestSuite((sequence.suite(), domnodes.suite(), datatypes.suite()))
  
if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())