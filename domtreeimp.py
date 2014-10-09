from types import BooleanType, FloatType
from operator import lt, le, eq, ne, ge, gt, add, div, mod, mul, sub, or_, and_
from itertools import chain, ifilter, imap, repeat
from xml.dom import Node
from datamodel import any, boolean, isaSequence, number, string, unPack, allDescendants, allDescendantsAndSelf

def shout(message, value) :
  print message
  return value      

class Counter :

  def __init__(self, iterator) :
    self.iterator = iterator
    self.position = 0
    self._size = None
    
  def __iter__(self) :
    return self
    
  def next(self) :
    if self._size == None :
      node = self.iterator.next()
    else :
      node = self.copy.next()
    self.position += 1
    #print self.position
    #return node
    return (node, self.position, self)
      
  #def __getattr__(self, name) :
  #  if name == "size" :
  #    if self._size == None :
  #      l = list(self.iterator)
  #      self._size = position + len(l)
  #      self.copy = iter(l)
  #    return self._size
  #  else :
  #    raise AttributeError
      
  def __float__(self) :
    if self._size == None :
      l = list(self.iterator)
      self._size = self.position + len(l)
      self.copy = iter(l)
    return float(self._size)


def root() :
  def root_(node, env) :
    if node.nodeType == Node.DOCUMENT_NODE :
      return [node]
    else :
      return [node.ownerDocument]
  return root_
  
def filterExpr(expr, predicates) :
  return addPredicates(expr, predicates)

def predicate(expr) :
  def predicateTest(node, predicate_value) :
    unpacked = unPack(predicate_value)
    if type(unpacked) == FloatType :
      return unpacked == node[1]
    else :
      return boolean(unpacked)
  return (lambda front :
      (lambda node, env :
          imap(
              lambda n :
                  n[0],
              ifilter(
                  lambda n : 
                      predicateTest(n, expr(n, env)),
                  Counter(
                      front(node, env))))))
  
def addPredicates(expr, predicate_list) :
  if len(predicate_list) == 0 :
    return expr
  return addPredicates(predicate_list[0](expr), predicate_list[1:])
   
def step(axis, node_test, predicates) :
  return addPredicates(
      (lambda node, env :
          node_test(
              axis(node),
              env)),
      predicates)

def child() :
  return lambda node : node.childNodes
  
def descendant() :
  return lambda node : allDescendants(node)

def attribute() :
  def attribute_(node) :
    n = 0
    while n < node.attributes.length :
      yield node.attributes.item(n)
      n += 1
  return attribute_
  
def parent() :
  return lambda node : [node.parentNode]
  
def self() :
  def self_(node) :
    yield node
  return self_
  
def descendant_or_self() :
  def descendant_or_self_(node) :
    return allDescendantsAndSelf(node)
  return descendant_or_self_

axis_list = {
    "child" : child,
    "descendant" : descendant,
    "attribute" : attribute,
    "parent" : parent,
    "self" : self,
    "descendant-or-self" : descendant_or_self,
}
  
def axis(name):
  return axis_list[name]()
         
def _nameTest(ns, name) :
  if ns == None :
    if name == "*" :
      return lambda node : True
    return lambda node : node.nodeName == name
  return lambda node : ( (ns == "*" or ns == node.namespaceURI) 
                         and 
                         (name == "*" or name == node.localName))

def nameTest(full_name) :
  parts = full_name.split(":")
  if len(parts) == 1 :
    ns = None
    name = parts[0]
  else :
    ns = parts[0]
    name = parts[1]
  return (lambda node_list, env : 
      ifilter(
          _nameTest(
              env.nsMap[ns],
              name),
          ifilter(
              lambda node : (node.nodeType == Node.ELEMENT_NODE or
                             node.nodeType == Node.ATTRIBUTE_NODE),
              node_list)))
              
def typeTest(nodeType) :
  def typeTest_(node) :
    return node.nodeType == nodeType
  return typeTest_

def comment(literal) :
  def commentFilter(node_list, env) :
    return ifilter(typeTest(Node.COMMENT_NODE), node_list)
  return commentFilter
    
  
def text(literal) :
  def textFilter(node_list, env) :
    return ifilter(typeTest(Node.TEXT_NODE), node_list)
  return textFilter
  
def processing_instruction(literal) :
  pass

node_types = [
    Node.ELEMENT_NODE,
    Node.COMMENT_NODE,
    Node.PROCESSING_INSTRUCTION_NODE,
    Node.TEXT_NODE,
    Node.DOCUMENT_NODE]
  
def node(literal) :
  def nodeFilter(node_list, env) :
    return [n for n in node_list if n.nodeType in node_types]
  return nodeFilter
  
node_type_list = {
  "comment" : comment,
  "text" : text,
  "processing_instruction" : processing_instruction,
  "node" : node
}

def nodeType(name, literal) :
  return node_type_list[name](literal)
                    
def pathExpr(path) :
  return (lambda node, env : evaluatePath(path, [node[0]], env))
  
def createNodeSetCapableOperator(operator) :
  def op(i1) :
    return lambda i2 : operator(i1, i2)
  def nodeSetCapableOperator(i1, i2) :
    i1 = unPack(i1)
    i2 = unPack(i2)
    type1 = type(i1)
    type2 = type(i2)
    if type1 == BooleanType or type2 == BooleanType :
      return operator(boolean(i1),boolean(i2))
    if isaSequence(i1) :
      if isaSequence(i2) :
        i2 = list(i2)
        return any(i1, lambda i : any(i2, op(i)))
      return any(i1, op(i2))
    if isaSequence(i2) :
      return any(i2, op(i1))
    return operator(i1,i2)
  return nodeSetCapableOperator
    
def createEqualityOperator(operator) :
  def equalityOperator(i1, i2) :
    type1 = type(i1)
    type2 = type(i2)
    if type1 == BooleanType or type2 == BooleanType :
      return operator(boolean(i1), boolean(i2))
    if type1 == FloatType or type2 == FloatType :
      return operator(number(i1), number(i2))
    return operator(string(i1), string(i2))
  return equalityOperator
  
def createArithmeticOperator(operator) :
  def relationalOperator(i1, i2) :
    return operator(number(i1), number(i2))
  return relationalOperator
 
def createXPathOperator(op) :
  def XPathOperator(arg1, arg2) :
    return (lambda node, env :
        [op(
            arg1(node, env),
            arg2(node, env))
         ])
  return XPathOperator

def createBooleanOperator(operator) :
  def booleanOperator(i1, i2) :
    return operator(boolean(i1), boolean(i2))
  return booleanOperator
  
def createUnionOperator(arg1, arg2) :
  def unionOperator(node, env) :
    return chain(
        arg1(node, env),
        arg2(node, env))
  return unionOperator

operator_map = {
    "<" : createXPathOperator(createNodeSetCapableOperator(createArithmeticOperator(lt))),
    "<=" : createXPathOperator(createNodeSetCapableOperator(createArithmeticOperator(le))),
    "=" : createXPathOperator(createNodeSetCapableOperator(createEqualityOperator(eq))),
    "!=" : createXPathOperator(createNodeSetCapableOperator(createEqualityOperator(ne))),
    ">=" : createXPathOperator(createNodeSetCapableOperator(createArithmeticOperator(ge))),
    ">" : createXPathOperator(createNodeSetCapableOperator(createArithmeticOperator(gt))),
    
    "+" : createXPathOperator(createArithmeticOperator(add)),
    "-" : createXPathOperator(createArithmeticOperator(sub)),
    "div" : createXPathOperator(createArithmeticOperator(div)),
    "mod" : createXPathOperator(createArithmeticOperator(mod)),
    "*" : createXPathOperator(createArithmeticOperator(mul)),

    "or" : createXPathOperator(createBooleanOperator(or_)),
    "and" : createXPathOperator(createBooleanOperator(and_)),
    
    "|" : createUnionOperator,
}

def binaryOperator(name, expr1, expr2) :
  return operator_map[name](expr1, expr2)

def negative(expr) :
  def negative_(node, env) :
    return - number(expr(node, env))
  return negative_
  
def Number(n) :
  n = float(n)
  return (lambda node, env : [n])
  
def Literal(l) :
  return (lambda node, env : [l])
  
def function(name, args) :
  def evaluateFunction(node, env) :
    return env.functions[name](node, map(lambda a : a(node,env), args), env)
  return evaluateFunction
  
def argument(expr) :
  return expr
      

def evaluatePartOnElement(part, node, env) :
  return part(node, env)
  
def evaluatePath(expr, node_list, env) :
  if len(expr) == 0 :
    return node_list
  else :
    return evaluatePath(
               expr[1:],
               chain(
                   *imap(
                       evaluatePartOnElement,
                       repeat(expr[0]),
                       node_list,
                       repeat(env))),
               env)
               
def XPathExpression(expr) :
  return (lambda node, env : unPack(expr((node, 1, 1), env)))
