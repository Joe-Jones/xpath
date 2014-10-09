
class trace:

  def __init__(self, to_trace) :
    self.to_trace = to_trace
    
  def __getattr__(self, name) :
    result = getattr(self.to_trace, name)
    print "access to attribute %s.%s, returning %s" % (repr(self.to_trace),
                                                      name, repr(result))
    return trace(result)
    
  def __getitem__(self, key) :
    return self.to_trace[key]
    
  def __call__(self, *rest) :
    print repr(self.to_trace)
    return self.to_trace.__call__(*rest)