import operator
import datamodel

#import itertools

def boolean(context, args, env) :
  yield datamodel.boolean(args[0])

def concat(context, args, env) :
  yield reduce(operator.concat, [datamodel.string(s) for s in args], u"") 
  
def contains(context, args, env) :
  yield datamodel.string(args[0]).find(datamodel.string(args[1])) != -1
  
def count(context, args, env) :
  yield float(reduce(lambda x, y : x+1, args[0], 0)) #Mabey there is a better way

def false(context, args, env) :
  yield False
  
def last(context, args, env) :
  yield float(context[2])
  
def local_name(context, args, env) :
  if len(args) > 0 :
    yield  datamodel.unPack(args[0]).next().localName
  else :
    yield context[0].localname
  
def xpath_function_not(context, args, env) :
  yield not datamodel.boolean(args[0])
  
def number(context, args, env) :
  if len(args) > 0 :
    yield datamodel.number(args[0])
  else :
    yield datamodel.number(context[0])
  
def position(context, args, env) :
  yield float(context[1])
  
def xpath_function_round(context, args, env) :
  yield float(round(datamodel.number(args[0])))
  
def starts_with(context, args, env) :
  pass
  
def string(context, args, env) :
  if len(args) > 0 :
    yield datamodel.string(args[0])
  else :
    yield datamadel.string(context[0])
    
def string_length(context, args, env) :
  if len(args) > 0 :
    return float(len(datamodel.string(args[0])))
  else :
    return float(len(datamodel.string(context[0])))

def true(context, args, env) :
  yield True


function_list = {
    "boolean" : boolean,
    "concat" : concat,
    "contains" : contains,
    "count" : count,
    "false" : false,
    "last" : last,
    "local-name" : local_name,
    "not" : xpath_function_not,
    "number" : number,
    "position" : position,
    "round" : xpath_function_round,
    "string" : string,
    "string-length" : string_length,
    "true" : true
}
