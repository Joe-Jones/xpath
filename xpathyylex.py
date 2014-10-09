import re
from xpathc import *

NCName = "[a-zA-Z_][a-zA-Z0-9_.-]*"
QName = "(%s:)?%s" % (NCName, NCName)
S = "[\t\n\r ]"

INITIAL = 0
OPERATOR = 1

ASCII = "ascii"
JUMP = "jump"
IGNORE = "ignore"

class XPathLexer :

    def __init__(self, query_string) :
        self.states = {
            INITIAL: [
                ("%s" % NCName, NCNAME, INITIAL),
                ("$%s*%s" % (S, QName), VARIABLE_REF, INITIAL),
                ("%s%s*\\(" % (NCName, S), FUNCTION_NAME, INITIAL),
                ("%s%s*::" % (NCName, S), AXIS_NAME, INITIAL),
                ("\/\/", DOUBLE_SLASH, INITIAL),
                ("\.\.", DOUBLE_DOT, INITIAL),
                ("!=", NEQ, INITIAL),
                ("<=", LTEQ, INITIAL),
                (">=", GTEQ, INITIAL),
                ("[0-9]+(\\.[0-9]+)?|(\\.[0-9]+)", NUMBER, OPERATOR),
                ("(\"[^\"]*\")|('[^']*')", LITERAL, INITIAL),
                ("\)", ASCII, OPERATOR),
                ("%s*" % S, IGNORE, INITIAL),
                (".", ASCII, INITIAL)],
            OPERATOR: [
                ("or", OR, INITIAL),
                ("and", AND, INITIAL),
                ("\\*", MUL, INITIAL),
                ("mod", MOD, INITIAL),
                ("div", DIV, INITIAL),
                ("%s*" %S, IGNORE, OPERATOR),
                (".", JUMP, INITIAL)]}
        for state in self.states :
            for n in range(len(self.states[state])) :
                s = self.states[state][n]
                self.states[state][n] = (re.compile(s[0]), s[1], s[2])
        self.state = INITIAL
        self.query_string = query_string
        #foo ="Hi there"
        #print "state : ", state

    def __call__(self) :
        #print s
        while True :
            #print foo
            longest_pattern = None
            length = 0
            value = ''
            for rule in self.states[self.state] :
                #print foo
                match = rule[0].match(self.query_string)
                if match and len(match.group()) > length:
                    length = len(match.group())
                    longest_pattern = rule
                    value = match.group()
            if length == 0 :
                #print "End"
                return 0, None
            if longest_pattern[1] == IGNORE :
                self.query_string = self.query_string[length:]
                self.state = longest_pattern[2]
                #print "Ignore", self.state, repr(value)
                continue
            if longest_pattern[1] == JUMP :
                self.state = longest_pattern[2]
                #print "Jump"
                continue
            self.state =  longest_pattern[2]
            if longest_pattern[1] == ASCII :
                self.query_string = self.query_string[length:]
                #print "c", value, self.state
                return ord(value), None
            #print value, self.state
            self.query_string = self.query_string[length:]
            return longest_pattern[1], value
    


