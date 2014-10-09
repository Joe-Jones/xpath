def root() :
  return lambda imp : imp.root()
   
def step(axis, node_test, predicates) :
  #print predicates
  return lambda imp : imp.step(axis(imp), node_test(imp), execute(predicates,imp))

def axis(name) :
  return lambda imp : imp.axis(name[:-2].strip())
  
def nameTest(name) :
  return lambda imp : imp.nameTest(name)
  
def nodeType(name, literal=None) :
  return lambda imp : imp.nodeType(name[:-1].strip(), literal)
  
def predicate(expr) :
  return lambda imp : imp.predicate(expr(imp))
  
def pathExpr(path) :
  return lambda imp : imp.pathExpr(execute(path,imp))
  
def filterExpr(expr, predicates) :
  return lambda imp : imp.filterExpr(expr(imp), execute(predicates, imp))
  
def function(name, args) :
  return lambda imp : imp.function(name[:-1].strip(), execute(args, imp))
  
def variableRef(name) :
  return lambda imp : imp.variableRef(name[1:].strip())
  
def argument(expr) :
  return lambda imp : imp.argument(expr(imp))
  
def binaryOperator(name, expr1, expr2) :
  return lambda imp : imp.binaryOperator(name, expr1(imp), expr2(imp))
  
def negative(expr) :
  return lambda imp : imp.negative(expr(imp))
  
def Number(n) :
  #print "a number ", n
  return lambda imp : imp.Number(n)
  
def Literal(l) :
  return lambda imp : imp.Literal(l[1:-1])

def XPathExpression(expr) :
  return lambda imp : imp.XPathExpression(expr(imp))
    
def execute(tree, imp) :
  return map(lambda i : i(imp), tree)
  
