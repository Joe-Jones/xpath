from domxpath import Compile, Environment


class XPath :

  def __init__(self, expression, reference) :
    self.xpath = Compile(expression)
    
  def setParameter(self, name, value) :
    pass
    
  def setNameSpace(self, prefix, name_space) :
    pass
    
  def execute(self, dom) :
    pass
    
class Result :

  def __init__(self) :
    pass
    
  def isaString(self) :
    return pass
    
  def isaNumber(self) :
    return pass
    
  def isaBoolean(self) :
    return pass
    
  def isaNodeset(self) :
    pass
    
  def __str__(self) :
    pass
    
  def __int__(self) :
    pass
    
def __long__(self) :
  pass
  
def __float__(self) :
  pass
  
def __coerce__(self, other) :
  pass
  
def __len__(self) :
  pass
  
def __getitem__(self, key) :
  pass
  
def __iter__(self) :
  pass
