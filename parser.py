import ply.yacc as yacc
from xpathyylex import tokens, XPathLexer
from parserbackend import *

def p_input(p) :
  'input : expr'
  p[0] = XPathExpression(p[1])
  
def p_locationpath(p) :
  ''' locationpath : relativelocationpath
                   | absolutelocationpath '''
  p[0] = p[1]

def p_absolutelocationpath_root(p) :
  ''' absolutelocationpath : '/' '''
  p[0] = [root()]

def p_absolutelocationpath_path(p) :
  ''' absolutelocationpath : '/' relativelocationpath '''
  p[0] = [root()] + p[2]

def p_absolutelocationpath_abbreviated(p) :
  'absolutelocationpath : abbreviatedabsolutelocationpath'
  p[0] = p[1]

def p_relativelocationpath_step(p) :
  'relativelocationpath : step'
  p[0] = [p[1]]

def p_relativelocationpath_stepplus(p) :
  ''' relativelocationpath : relativelocationpath '/' step '''
  p[0] = p[1] + [p[3]]

def p_relativelocationpath_abbreviated(p) :
  ' relativelocationpath : abreviaterelativelocationpath '
  p[0] = p[1]

def p_step_normal(p) :
  'step : axisspecifier nodetest predicatelist'
  p[0] = step(p[1], p[2], p[3])

def p_step_abbreviated(p) :
  'step : abbreviatedstep'
  p[0] = p[1]

def p_predicatelist_empty(p) :
  'predicatelist : '
  p[0] = []

def p_predicatelist_nonempty(p) :
  'predicatelist : predicatelist predicate'
  p[0] = p[1] + [p[2]]
  
def p_axisspecifier_a(p) :
  ' axisspecifier : AXISNAME '
  p[0] = axis(p[1])
  
def p_axisspecifier_b(p) :
  ' axisspecifier : abbreviatedaxisspecifier '
  p[0] = p[1]

def p_nodetest_name(p) :
  'nodetest : nametest '
  p[0] = nameTest(p[1])

def p_nodetest_function(p) :
  ''' nodetest : FUNCTIONNAME ')' '''
  p[0] = nodeType(p[1])

def p_nodetest_functionarg(p) :
  ''' nodetest : FUNCTIONNAME LITERAL ')' '''
  p[0] = nodeType(p[1], p[2])
  
def p_predicate(p) :
  ''' predicate : '[' predicateexpr ']' '''
  p[0] = predicate(p[2])

def p_predicateexpr(p) :
  ''' predicateexpr : expr '''
  p[0] = p[1]
  
def p_abbreviatedabsolutelocationpath(p) :
  ' abbreviatedabsolutelocationpath : DOUBLESLASH relativelocationpath '
  p[0] = [root(), step(axis("descendant-or-self::"), nodeType("node(", 0), [])] + p[2]

def p_abreviaterelativelocationpath(p) :
  ' abreviaterelativelocationpath : relativelocationpath DOUBLESLASH step '
  p[0] = p[1] + [step(axis("descendant-or-self::"), nodeType("node(", 0), []), p[3]]
  
def p_abbreviatedstep_dot(p) :
  ''' abbreviatedstep : '.' '''
  p[0] = step(axis("self::"), nodeType("node("), [])
    
def p_abbreviatedstep_doubledot(p) :
  ' abbreviatedstep : DOUBLEDOT '
  p[0] = step(axis("parent::"), nodeType("node("), [])
    
def p_abbreviatedaxisspecifier_blank(p) :
  'abbreviatedaxisspecifier : '
  p[0] = axis("child::")
    
def p_abbreviatedaxisspecifier_at(p) :
  '''abbreviatedaxisspecifier : '@' '''
  p[0] = axis("attribute::")
  
def p_expr(p) :
  'expr : orexpr'
  p[0] = p[1]

def p_primaryexpr_var(p) :
  ''' primaryexpr : VARIABLEREF '''
  p[0] = variableReef(p[1])
  
def p_primaryexpr_expr(p) :
  ''' primaryexpr : '(' expr ')' '''
  p[0] = p[2]

def p_primaryexpr_literal(p) :
  ''' primaryexpr : LITERAL '''
  p[0] = Literal(p[1])

def p_primaryexpr_number(p) :
  ''' primaryexpr : NUMBER'''
  p[0] = Number(p[1])
  
def p_primaryexpr_function(p) :
  ''' primaryexpr : functioncall'''
  p[0] = p[1]
  
def p_functioncall(p) :
  ''' functioncall : FUNCTIONNAME argumentlist ')' '''
  p[0] = function(p[1], p[2])
  
def p_argumentlist_empty(p) :
  ''' argumentlist : '''
  p[0] = []
  
def p_argumentlist_one(p) :
  ''' argumentlist : argument'''
  p[0] = [p[1]]
  
def p_argumentlist_many(p) :
  ''' argumentlist : argumentlist ',' argument '''
  p[0] = p[1] + [p[3]]
  
def p_argument(p) :
  ''' argument : expr '''
  p[0] = argument(p[1])
  
def p_unionexpr_path(p) :
  ''' unionexpr : pathexpr '''
  p[0] = p[1]
  
def p_unionexpr_bar(p) :
  ''' unionexpr : unionexpr '|' pathexpr '''
  p[0] = binaryOperator('|', p[1], p[3])
  
def p_pathexpr_location(p) :
  ''' pathexpr : locationpath '''
  p[0] = pathExpr(p[1])
  
def p_pathexpr_filter(p) :
  ''' pathexpr : filterexpr '''
  p[0] = p[1]
  
#def p_pathexpr_1(p) :
#  ''' pathexpr : '''
#  p[0] = 
  
#def p_pathexpr_2(p) :
#  ''' pathexpr : '''
#  p[0] = 
  
def p_filterexpr_one(p):
  ''' filterexpr : primaryexpr '''
  p[0] = p[1]
  
def p_filterexpr_two(p):
  ''' filterexpr : primaryexpr predicatelist'''
  p[0] = filterExpr(p[1], p[2])

def p_orexpr_a(p):
  ''' orexpr : andexpr'''
  p[0] = p[1]
  
def p_orexpr_b(p):
  ''' orexpr : orexpr OR andexpr'''
  p[0] = binaryOperator("or", p[1], p[3])
  
def p_andexpr_a(p):
  ''' andexpr : equalityexpr'''
  p[0] = p[1]
  
def p_andexpr_b(p):
  ''' andexpr : andexpr AND equalityexpr'''
  p[0] = binaryOperator("and", p[1], p[3])
  
def p_equalityexpr_a(p):
  ''' equalityexpr : relationalexpr'''
  p[0] = p[1]
  
def p_equalityexpr_b(p):
  ''' equalityexpr : equalityexpr '=' relationalexpr'''
  p[0] = binaryOperator("=", p[1], p[3])
  
def p_equalityexpr_c(p):
  ''' equalityexpr : equalityexpr NEQ relationalexpr'''
  p[0] = binaryOperator("!=", p[1], p[3])
  
def p_relationalexpr_a(p) :
  ''' relationalexpr : additiveexpr '''
  p[0] = p[1]
  
def p_relationalexpr_b(p) :
  ''' relationalexpr : relationalexpr '<' additiveexpr '''
  p[0] = binaryOperator("<", p[1], p[3])
  
def p_relationalexpr_c(p) :
  ''' relationalexpr : relationalexpr '>' additiveexpr '''
  p[0] = binaryOperator(">", p[1], p[3])
    
def p_relationalexpr_d(p) :
  ''' relationalexpr : relationalexpr LTEQ additiveexpr '''
  p[0] = binaryOperator("<=", p[1], p[3])
    
def p_relationalexpr_e(p) :
  ''' relationalexpr : relationalexpr GTEQ additiveexpr '''
  p[0] = binaryOperator(">=", p[1], p[3])
    
def p_additiveexpr_a(p) :
  ''' additiveexpr : multiplicativeexpr '''
  p[0] = p[1]
  
def p_additiveexpr_b(p) :
  ''' additiveexpr : additiveexpr '+' multiplicativeexpr '''
  p[0] = binaryOperator("+", p[1], p[3])
  
def p_additiveexpr_c(p) :
  ''' additiveexpr : additiveexpr '-' multiplicativeexpr '''
  p[0] = binaryOperator("-", p[1], p[3])
  
def p_multiplicativeexpr_a(p) :
  ''' multiplicativeexpr : unaryexpr '''
  p[0] = p[1]
  
def p_multiplicativeexpr_b(p) :
  ''' multiplicativeexpr : multiplicativeexpr MUL unaryexpr '''
  p[0] = binaryOperator("*", p[1], p[3])
  
def p_multiplicativeexpr_c(p) :
  ''' multiplicativeexpr : multiplicativeexpr DIV unaryexpr '''
  p[0] = binaryOperator("div", p[1], p[3])
  
def p_multiplicativeexpr_d(p) :
  ''' multiplicativeexpr : multiplicativeexpr MOD unaryexpr '''
  p[0] = binaryOperator("mod", p[1], p[3])
  
def p_unaryexpr_a(p) :
  ''' unaryexpr : unionexpr '''
  p[0] = p[1]
  
def p_unaryexpr_b(p) :
  ''' unaryexpr : '-' unaryexpr '''
  p[0] = negative(p[2])
  
def p_nametest_a(p) :
  ''' nametest : '*' '''
  p[0] = '*'
  
def p_nametest_b(p) :
  ''' nametest : NCNAME ':' '*' '''
  p[0] = [p[1], p[2], p[3]]
  
def p_nametest_c(p) :
  ''' nametest : qname'''
  p[0] = p[1]

def p_qname_a(p) :
  ''' qname : NCNAME ':' NCNAME '''
  p[0] = p[1] + ':' + p[3]
  
def p_qname_b(p) :
  ''' qname : NCNAME '''
  p[0] = p[1]

def parse(expression) :
  parser = yacc.yacc()
  lexer = XPathLexer()
  return parser.parse(expression, lexer=lexer)
