import xpathc
import domtreeimp
from functions import function_list
from xml.dom.ext import Print
import parserbackend
from xpathyylex import XPathLexer


class Environment :

  def __init__(self, nsMap = {}, variables = {}, functions = {}) :
    self.nsMap = dict(nsMap)
    self.nsMap[None] = None
    self.nsMap["*"] = "*"
    self.functions = function_list

def Compile(e) :
  #l = XPathLexer(e)
  #print dir(l), str(l.func_closure), l.func_dict
  #parser = xpathc.new()
  #parser.verbose = True
  #expression = parser.parse(e)
  expression = xpathc.parse(parserbackend.__dict__, XPathLexer(e))
  return expression(domtreeimp)
  #return lambda node, nsMap : domtreeimp.evaluate(expression, node, nsMap)
  
doc = """<d_n_d_players>
  <player>
    <name>Joe</name>
    <character>Rasputin</character>
  </player>
  <player>
    <name>Scot</name>
    <character>elstar</character>
  </player>
</d_n_d_players>"""

doc = """<?xml version="1.0"?>
<root>
  <anItem>1</anItem>
  <anItem>2</anItem>
</root>"""

doc = """<?xml version="1.0"?>
<root hi="there">
  <anItem hi="there">1</anItem>
  <anItem hi="there" now="again">2</anItem>
</root>"""

doc2 = """<?xml version="1.0"?><one><two>Three</two><two/></one>"""

  
if __name__ == "__main__" :
  from xml.dom.ext.reader import Sax2
  from xml.dom.minidom import parseString
  from trace import trace
  reader = Sax2.Reader()
  doc1 = reader.fromString(doc)
  doc2 = parseString(doc)
  #doc = reader.fromSt("DnD.xml")
  #expr = Compile("/d_n_d_players/player/../../d_n_d_players/player/character")
  expr = Compile("count(/descendant::*/attribute::*) = 4")
  #expr = Compile(" 2 + 5 * 3")
  #for n in range(1) :
  #  if n % 100 == 0 :
  #    print ".",
  #  for i in expr(doc, Environment()) :
  #    Print (i)
  #    print
  #    #pass
  result = expr(trace(doc2), Environment())
  print repr(result)
  #for r in result:
  #  print repr(r)
  #expr(test_doc, Environment())
  
