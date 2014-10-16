from flask import Flask, Response, request
from jinja2 import Environment, PackageLoader
import json
import domxpath
from xml.dom.minidom import parse
import sys
import os
import uuid

class Session:
  
  def __init__(self) :
    self.env = domxpath.Environment()
  
  def setDom(self, dom) :
    self.dom = dom
    
  def setXpath(self, xpath) :
    self.expression  = domxpath.Compile(xpath)
    return self.expression is not None
  
  def run(self) :
    fn = self.expression
    result = fn(self.dom, self.env)
    as_a_list = []
    if hasattr(result, '__iter__') :
      for r in result :
        as_a_list.append(r.toxml().replace("<", "&lt;").replace("\n", "<br>"))
      return as_a_list
    else :
      return [result]

global sessions
sessions = {}

app = Flask(__name__)
env = Environment(loader=PackageLoader('__main__', './'))

example_dom = parse('example.xml')

@app.route("/demo.js")
def js() :
  template = env.get_template('demo.js')
  return Response(template.render(), mimetype='application/javascript')

@app.route("/")
def hello():
  sessionkey = str(uuid.uuid1())
  session = Session()
  session.setDom(example_dom)
  session.setXpath("/")
  sessions[sessionkey] = session
  template = env.get_template('demo.html')
  return template.render(sessionkey = sessionkey)
  
@app.route('/run/<sessionkey>')
def run(sessionkey) :
  session = sessions[sessionkey]
  return json.dumps(session.run())
  
@app.route('/compile/<sessionkey>', methods=["POST"])
def compile(sessionkey) :
  session = sessions[sessionkey]
  if session.setXpath(request.form["path"]) is None :
    return "F"
  else :
    return "T"

if __name__ == "__main__":
  pid = os.fork() 
  if pid > 0:
    sys.exit(0)
  #os.chdir("/") 
  os.setsid() 
  os.umask(0) 
  pid = os.fork() 
  if pid > 0: 
    sys.exit(0) 
  
  app.run(port=8888,  debug=True)

