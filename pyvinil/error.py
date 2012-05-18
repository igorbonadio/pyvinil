import exceptions

class VHDError(exceptions.Exception):
  def __init__(self, msg):
    self.msg = msg
    
  def __str__(self):
    return "VHDError: " + self.msg
