%{
  #include "Python/Python.h"
  #define YYSTYPE PyObject*
  #include "xpathmodule.h"
%}

%pure-parser
%parse-param {ImportTable* functions}
%parse-param {PyObject* lex_object}
%parse-param {PyObject** result}
%lex-param {PyObject* lex_object}


%token NCNAME
%token FUNCTION_NAME
%token OR
%token AND
%token NEQ
%token LTEQ
%token GTEQ
%token NUMBER
%token LITERAL
%token MOD
%token DIV
%token MUL
%token AXIS_NAME
%token DOUBLE_SLASH
%token DOUBLE_DOT
%token VARIABLE_REF


%%

input: 
          Expr {
              PyObject *arglist;
              arglist = Py_BuildValue("(O)", $1);
              *result = PyEval_CallObject(functions->XPathExpression, arglist);
              Py_DECREF(arglist);
              YYACCEPT }
;

/* [1] */
LocationPath: 
          RelativeLocationPath
        | AbsoluteLocationPath
;

/* [2] */
AbsoluteLocationPath:
          '/' {
              //printf("Creating a root node\n");
              PyObject *arglist;
              $$ = PyList_New(1);
              arglist = Py_BuildValue("()");
              PyList_SET_ITEM($$, 0, PyEval_CallObject(functions->root, arglist));
              Py_DECREF(arglist); }
        | '/' RelativeLocationPath {
              //printf("Prppending a root node to a relative location\n");
              PyObject *arglist;
              arglist = Py_BuildValue("()");
              PyList_Insert($2, 0, PyEval_CallObject(functions->root, arglist));
              $$ = $2;
              Py_INCREF($2);
              Py_DECREF(arglist); }
        | AbbreviatedAbsoluteLocationPath
;

/* [3] */
RelativeLocationPath:
          Step {
              //printf("1\n");
              $$ = PyList_New(1);
              PyList_SET_ITEM($$, 0, $1);
              Py_INCREF($1); }
        | RelativeLocationPath '/' Step {
              //printf("2\n");
              PyList_Append($1,$3);
              $$ = $1;
              Py_INCREF($1); }
        | AbbreviatedRelativeLocationPath
;

/* [4] */
Step:
          AxisSpecifier NodeTest PredicateList {
              //printf("Hi there from tne step\n");
              PyObject *arglist;
              arglist = Py_BuildValue("(O,O,O)", $1, $2, $3);
              $$ = PyEval_CallObject(functions->step, arglist);
              Py_DECREF(arglist); }
        | AbbreviatedStep
;

   /* <!--<production>
      <non-terminal>FullStep</non-terminal>-->*/
    
PredicateList:
          {
              $$ = PyList_New(0); }
        | PredicateList Predicate {
              PyList_Append($1, $2);
              $$ = $1;
              Py_INCREF($$); }
;
    
/* [5] */
AxisSpecifier:
          AXIS_NAME {
              //printf("Hi there from axis specifier");
              PyObject *arglist;
              arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist); }
        | AbbreviatedAxisSpecifier
;

/* [7] */
NodeTest:
          NameTest {
              //printf("Hi from NodeTest\n");
              PyObject *arglist;
              arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->nameTest, arglist);
              Py_DECREF(arglist); }
        | FUNCTION_NAME ')' {
              PyObject *arglist;
              arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->nodeType, arglist);
              Py_DECREF(arglist); }
        | FUNCTION_NAME LITERAL ')' {
              PyObject *arglist;
              arglist = Py_BuildValue("(O,O)", $1, $2);
              $$ = PyEval_CallObject(functions->nodeType, arglist);
              Py_DECREF(arglist); }
;
    
/* [8] */
Predicate:
          '[' PredicateExpr ']' {
              //$$ = $2;
              //Py_INCREF($$);
              PyObject *arglist = Py_BuildValue("(O)", $2);
              $$ = PyEval_CallObject(functions->predicate, arglist);
              Py_DECREF(arglist); }
;

/* [9] */
PredicateExpr:
          Expr
;
    
/* [10] */
AbbreviatedAbsoluteLocationPath:
          DOUBLE_SLASH RelativeLocationPath {
              PyObject *arglist, *root_part, *step_axis, *node_test,
                       *predicate_list, *the_step;
          
              PyObject *slash_part = PyList_New(2);
          
              arglist = Py_BuildValue("()");
              root_part = PyEval_CallObject(functions->root, arglist);
              Py_DECREF(arglist);
          
              arglist = Py_BuildValue("(s)", "descendant-or-self::");
              step_axis = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist);
          
              arglist = Py_BuildValue("(s,s)", "node(", 0);
              node_test = PyEval_CallObject(functions->nodeType, arglist);
              Py_DECREF(arglist);
          
              predicate_list = PyList_New(0);
 
              arglist = Py_BuildValue("(O,O,O)", step_axis, node_test, predicate_list);
              the_step = PyEval_CallObject(functions->step, arglist);
              Py_DECREF(step_axis);
              Py_DECREF(node_test);
              Py_DECREF(predicate_list);     
                  
              PyList_SetItem(slash_part, 0, root_part);
              PyList_SetItem(slash_part, 1, the_step);
          
              $$ = PySequence_Concat(slash_part, $2);
          
              Py_DECREF(slash_part); }
;

/* [11] */
AbbreviatedRelativeLocationPath:
          RelativeLocationPath DOUBLE_SLASH Step {
              PyObject *arglist, *step_axis, *node_test, *predicate_list, *the_step;
          
              PyObject *slash_part_and_step = PyList_New(2);
          
              arglist = Py_BuildValue("(s)", "descendant-or-self::");
              step_axis = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist);
          
              arglist = Py_BuildValue("(s,s)", "node(", 0);
              node_test = PyEval_CallObject(functions->nodeType, arglist);
              Py_DECREF(arglist);
          
              predicate_list = PyList_New(0);
          
              arglist = Py_BuildValue("(O,O,O)", step_axis, node_test, predicate_list);
              the_step = PyEval_CallObject(functions->step, arglist);
              Py_DECREF(step_axis);
              Py_DECREF(node_test);
              Py_DECREF(predicate_list);     
          
              PyList_SetItem(slash_part_and_step, 0, the_step);
              PyList_SetItem(slash_part_and_step, 1, $3);
              Py_INCREF($3);
          
              $$ = PySequence_Concat($1, slash_part_and_step);
          
              Py_DECREF(slash_part_and_step); }
;

/* [12] */
AbbreviatedStep:
          '.' {
              PyObject *arglist, *step_axis, *node_test, *predicate_list;
          
              arglist = Py_BuildValue("(s)", "self::");
              step_axis = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist);
          
              arglist = Py_BuildValue("(s,s)", "node(", 0);
              node_test = PyEval_CallObject(functions->nodeType, arglist);
              Py_DECREF(arglist);
          
              predicate_list = PyList_New(0);
          
              arglist = Py_BuildValue("(O,O,O)", step_axis, node_test, predicate_list);
              $$ = PyEval_CallObject(functions->step, arglist);
              Py_DECREF(step_axis);
              Py_DECREF(node_test);
              Py_DECREF(predicate_list); }
        | DOUBLE_DOT {
              PyObject *arglist, *step_axis, *node_test, *predicate_list;
          
              arglist = Py_BuildValue("(s)", "parent::");
              step_axis = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist);
          
              arglist = Py_BuildValue("(s,s)", "node(", 0);
              node_test = PyEval_CallObject(functions->nodeType, arglist);
              Py_DECREF(arglist);
           
              predicate_list = PyList_New(0);
          
              arglist = Py_BuildValue("(O,O,O)", step_axis, node_test, predicate_list);
              $$ = PyEval_CallObject(functions->step, arglist);
              Py_DECREF(step_axis);
              Py_DECREF(node_test);
              Py_DECREF(predicate_list); }
;

/* [13] */
AbbreviatedAxisSpecifier:
          {
              PyObject *arglist;
              arglist = Py_BuildValue("(s)", "child::");
              $$ = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist); }
        | '@' {
              PyObject *arglist;
              arglist = Py_BuildValue("(s)", "attribute::");
              $$ = PyEval_CallObject(functions->axis, arglist);
              Py_DECREF(arglist); }
;
    
/* [14] */
Expr:
          OrExpr
;
    
/* [15] */
PrimaryExpr:
          VARIABLE_REF {
              PyObject *arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->variableRef, arglist);
              Py_DECREF(arglist); }
        | '(' Expr ')' {
              $$=$2;
              Py_INCREF($$); }
        | LITERAL {
              PyObject *arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->Literal, arglist);
              Py_DECREF(arglist); }
        | NUMBER {
              PyObject *arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->Number, arglist);
              Py_DECREF(arglist); }
        | FunctionCall
;
    
/* [16] */
FunctionCall:
          FUNCTION_NAME ArgumentList ')' {
              PyObject *arglist = Py_BuildValue("(O, O)", $1, $2);
              $$ = PyEval_CallObject(functions->function, arglist);
              Py_DECREF(arglist); }
;

ArgumentList:
          {
              $$ = PyList_New(0); }
        | Argument {
              $$ = PyList_New(0);
              PyList_Append($$, $1); }
        | ArgumentList ',' Argument {
              PyList_Append($1, $3);
              $$ = $1;
              Py_INCREF($$); }
;

/* [17] */
Argument:
          Expr {
              PyObject *arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->argument, arglist);
              Py_DECREF(arglist); }
;

/* [18] */
UnionExpr:
          PathExpr
        | UnionExpr '|' PathExpr {
              PyObject *arglist = Py_BuildValue("(s, O, O)", "|", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;
    
/* [19] */
PathExpr:
          LocationPath {
              PyObject *arglist = Py_BuildValue("(O)", $1);
              $$ = PyEval_CallObject(functions->pathExpr, arglist);
              Py_DECREF(arglist); }
        | FilterExpr {
              //printf("FilterExpr\n");
              $$=$1;
              Py_INCREF($$); }
        | FilterExpr '/' RelativeLocationPath
        | FilterExpr DOUBLE_SLASH RelativeLocationPath
;
    
/* [20] */
FilterExpr:
          PrimaryExpr
        | PrimaryExpr PredicateList {
              PyObject *arglist = Py_BuildValue("(O,O)", $1, $2);
              $$ = PyEval_CallObject(functions->filterExpr, arglist);
              Py_DECREF(arglist); }
;

/* [21] */
OrExpr:
          AndExpr
        | OrExpr OR AndExpr {
              PyObject *arglist = Py_BuildValue("(s, O, O)", "or", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;

/* [22] */
AndExpr:
          EqualityExpr
        | AndExpr AND EqualityExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "and", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;

/* [23] */
EqualityExpr:
          RelationalExpr
        | EqualityExpr '=' RelationalExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "=", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | EqualityExpr NEQ RelationalExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "!=", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;

/* [24] */
RelationalExpr:
          AdditiveExpr
        | RelationalExpr '<' AdditiveExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "<", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | RelationalExpr '>' AdditiveExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", ">", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | RelationalExpr LTEQ AdditiveExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "<=", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | RelationalExpr GTEQ AdditiveExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", ">=", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;
    
/* [25] */
AdditiveExpr:
          MultiplicativeExpr
        | AdditiveExpr '+' MultiplicativeExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "+", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | AdditiveExpr '-' MultiplicativeExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "-", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;
    
/* [26] */
MultiplicativeExpr:
          UnaryExpr
        | MultiplicativeExpr MUL UnaryExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "*", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | MultiplicativeExpr DIV UnaryExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "div", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
        | MultiplicativeExpr MOD UnaryExpr {
              PyObject *arglist = Py_BuildValue("(s,O,O)", "mod", $1, $3);
              $$ = PyEval_CallObject(functions->binaryOperator, arglist);
              Py_DECREF(arglist); }
;
   
/* [27] */
UnaryExpr:
          UnionExpr
        | '-' UnaryExpr {
              PyObject *arglist = Py_BuildValue("(O)", $2);
              $$ = PyEval_CallObject(functions->negative, arglist);
              Py_DECREF(arglist); }
;
    
/*    <!--[35]-->
   <!-- <production>
      <non-terminal>FunctionName</non-terminal>	   ::=   	QName - NodeType
    -->*/

/* [37] */
NameTest:
          '*' {
              $$ = Py_BuildValue("s", "*"); }
        | NCNAME ':' '*' {
              PyObject *temp = PySequence_Concat($1, $2);
              $$ = PySequence_Concat(temp, $3);
              Py_DECREF(temp); }
        | QName
;
    
QName:
          NCNAME ':' NCNAME {
              PyObject *temp, *colon;
              colon = Py_BuildValue("s", ":");
              temp= PySequence_Concat($1, colon);
              $$ = PySequence_Concat(temp, $3);
              Py_DECREF(temp);
              Py_DECREF(colon); }
        | NCNAME
;

%%




