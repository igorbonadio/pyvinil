from ctypes import *

class VHD:
  
  def __init__(self, vhd_pointer):
    if vhd_pointer.value is None:
      raise Exception("open/create")
    else:
      self.vhd_pointer = vhd_pointer
      self.vinil_dll = cdll.LoadLibrary("libvinil.dylib")
  
  @staticmethod
  def open(path):
    vinil_dll = cdll.LoadLibrary("libvinil.dylib")
    vinil_dll.vinil_vhd_open.argtypes = [c_char_p]
    vinil_dll.vinil_vhd_open.restype = c_void_p
    return VHD(c_void_p(vinil_dll.vinil_vhd_open(path)))
  
  def close(self):
    self.vinil_dll.vinil_vhd_close.argtypes = [c_void_p]
    self.vinil_dll.vinil_vhd_close(self.vhd_pointer);
    
  def read(self, count):
    self.vinil_dll.vinil_vhd_read.argtypes = [c_void_p, c_void_p, c_int]
    self.vinil_dll.vinil_vhd_read.restype = c_int
    buf = (c_char*512*count)()
    ret = ""
    if self.vinil_dll.vinil_vhd_read(self.vhd_pointer, buf, count) == 1:
      for i in buf:
         ret += str(i.value)
      return ret
    else:
      raise Exception("Read")
    
  def write(self, buf, count):
    self.vinil_dll.vinil_vhd_write.argtypes = [c_void_p, c_void_p, c_int]
    self.vinil_dll.vinil_vhd_write.restype = c_int
    if not self.vinil_dll.vinil_vhd_write(self.vhd_pointer, buf, count) == 1:
      raise Exception("Write")
    
  def tell(self):
    self.vinil_dll.vinil_vhd_tell.argtypes = [c_void_p]
    self.vinil_dll.vinil_vhd_tell.restype = c_longlong
    ret = self.vinil_dll.vinil_vhd_tell(self.vhd_pointer)
    if ret < 0:
      raise Exception("tell")
    return ret
    
  def seek(self, offset, origin):
    self.vinil_dll.vinil_vhd_seek.argtypes = [c_void_p, c_longlong, c_int]
    self.vinil_dll.vinil_vhd_seek.restype = c_int
    if not self.vinil_dll.vinil_vhd_seek(self.vhd_pointer, offset, origin) == 1:
      raise Exception("seek")
    
  def flush(self):
    self.vinil_dll.vinil_vhd_flush.argtypes = [c_void_p]
    self.vinil_dll.vinil_vhd_flush.restype = c_longlong
    if not self.vinil_dll.vinil_vhd_flush(self.vhd_pointer) == 1:
      raise Exception("flush")
