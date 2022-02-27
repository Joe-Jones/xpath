"""This module contains basic functions for quering the xpath data
model, and the building blocks for evaluating xpath exspresions.
"""

from types import InstanceType, BooleanType, FloatType, StringTypes
from itertools import ifilter, chain, imap
from operator import concat, lt, le, eq, ne, ge, gt

from xml.dom import Node

#Functions not directly related to the data model

def aggregate(function, seed, iterable) :
  "Generic function operating in a sequence"
  for i in iterable :
    seed = function(seed, i)
  return seed

def any(seq, pred=bool):
  "Returns True if pred(x) is True for at least one element in the iterable"
  for elem in ifilter(pred, seq):
    return True
  return False
  
#functions quereing information from the dom

def allDescendants(node) :
  for child in node.childNodes :
    yield child
    for descendant in allDescendants(child) :
     yield descendant

def allDescendantsAndSelf(node) :
  yield node
  for descendant in allDescendants(node) :
    yield descendant

use_node_value = [Node.ATTRIBUTE_NODE,     Node.TEXT_NODE, 
                  Node.CDATA_SECTION_NODE, Node.PROCESSING_INSTRUCTION_NODE,
                  Node.COMMENT_NODE ]
        
def string_value(node) :
  "This is the string-value that the xpath spec speaks of."
  if node.nodeType == Node.ELEMENT_NODE or node.nodeType == Node.DOCUMENT_NODE :
    return aggregate(
               concat,
               "",
               imap(lambda n : n.nodeValue,
                   ifilter(
                       lambda node : node.nodeType in [Node.TEXT_NODE, Node.CDATA_SECTION_NODE],
                       allDescendantsAndSelf(node)))
           )
  if node.nodeType in use_node_value :
    return node.nodeValue
  
  
#Casting xpath types, These functions can operate on packed objects

def unPack(i) :
  if type(i) is str :
    return i
  if not isaSequence(i) :
    return i
  try :
    first = iter(i).next()
  except StopIteration :
    return []
  t = type(first)
  if t is InstanceType :
    return chain([first], i)
  else : 
    return first
    
def isaSequence(i) :
  if type(i) is str :
    return False
  try :
    iter(i)
  except :
    return False;
  return True
  
def isEmptySequence(i) :
  "Only workes on unpacked sequences"
  return i == []

    
def boolean(n) :
  unpacked = unPack(n)
  if isaSequence(unpacked) :
    return not isEmptySequence(unpacked)
  t = type(unpacked)
  if t is bool :
    return unpacked
  if t is float :
    return unpacked != 0
  if t is str :
    return unpacked != ""
  raise "Hell"
  
def number(n) :
  unpacked = unPack(n)
  if isaSequence(unpacked) or type(unpacked) == InstanceType:
    return float(string(unpacked))
  t = type(unpacked)
  if t is bool :
    if unpacked : return float(1)
    else : return float(0)
  if t is float :
    return unpacked
  if t is str :
    return float(unpacked)
  raise "Hell"
  
def string(n) :
  unpacked = unPack(n)
  if isaSequence(unpacked) :
    if isEmptySequence(unpacked) :
      return u""
    else :
      return string_value(iter(unpacked).next())
  t = type(unpacked)
  if t is bool :
    if unpacked : return u"true"
    else : return u"false"
  if t is float :
    if unpacked % 1 == 0 :
      return  "%d" % unpacked
    else :
      return "%f" % unpacked
  if t is InstanceType :
    return string_value(unpacked)
  if t is str :
    return unpacked
  raise "Hell"    
