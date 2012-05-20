from ctypes import *

from pyvinil.utils import VinilDynamicLibrary
from pyvinil.error import VHDError

class VHDFooterStructure(Structure):
  _fields_ = [("cookie", c_char*8),
              ("features", c_uint),
              ("file_format_version", c_uint),
              ("data_offset", c_longlong),
              ("timestamp", c_uint),
              ("creator_application", c_char*4),
              ("creator_version", c_uint),
              ("creator_host_os", c_uint),
              ("original_size", c_longlong),
              ("current_size", c_longlong),
              ("disk_geometry", c_uint),
              ("disk_type", c_uint),
              ("checksum", c_uint),
              ("uuid", c_char*16),
              ("saved_state", c_char),
              ("reserved", c_char*427)]
              
class VinilVHDStructure(Structure):
  _fields_ = [("fd", c_void_p),
              ("footer", c_void_p)]

class VHD:
  
  def __init__(self, vhd_pointer):
    if vhd_pointer.value is None:
      raise VHDError("Can't open/create the vhd file")
    else:
      self.vhd_pointer = vhd_pointer
      self.vinil_dll = VinilDynamicLibrary().get_dynamic_library()
      self.opened = True
      self.footer = cast(cast(self.vhd_pointer, POINTER(VinilVHDStructure)).contents.footer, POINTER(VHDFooterStructure)).contents
  
  @staticmethod
  def open(path):
    vinil_dll = VinilDynamicLibrary().get_dynamic_library()
    vinil_dll.vinil_vhd_open.argtypes = [c_char_p]
    vinil_dll.vinil_vhd_open.restype = c_void_p
    return VHD(c_void_p(vinil_dll.vinil_vhd_open(path)))
  
  def close(self):
    if self.opened:
      self.vinil_dll.vinil_vhd_close.argtypes = [c_void_p]
      self.vinil_dll.vinil_vhd_close(self.vhd_pointer);
      self.opened = False
    
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
      raise VHDError("Can't read sectors from the vhd file")
    
  def write(self, buf, count):
    self.vinil_dll.vinil_vhd_write.argtypes = [c_void_p, c_void_p, c_int]
    self.vinil_dll.vinil_vhd_write.restype = c_int
    if not self.vinil_dll.vinil_vhd_write(self.vhd_pointer, buf, count) == 1:
      raise VHDError("Can't write sectors to the vhd file")
    
  def tell(self):
    self.vinil_dll.vinil_vhd_tell.argtypes = [c_void_p]
    self.vinil_dll.vinil_vhd_tell.restype = c_longlong
    ret = self.vinil_dll.vinil_vhd_tell(self.vhd_pointer)
    if ret < 0:
      raise VHDError("tell couldn't be executed")
    return ret
    
  def seek(self, offset, origin):
    self.vinil_dll.vinil_vhd_seek.argtypes = [c_void_p, c_longlong, c_int]
    self.vinil_dll.vinil_vhd_seek.restype = c_int
    if not self.vinil_dll.vinil_vhd_seek(self.vhd_pointer, offset, origin) == 1:
      raise VHDError("seek couldn't be executed")
    
  def flush(self):
    self.vinil_dll.vinil_vhd_flush.argtypes = [c_void_p]
    self.vinil_dll.vinil_vhd_flush.restype = c_longlong
    if not self.vinil_dll.vinil_vhd_flush(self.vhd_pointer) == 1:
      raise VHDError("flush couldn't be executed")
      
  def commit_structural_changes(self):
    self.vinil_dll.vinil_vhd_commit_structural_changes.argtypes = [c_void_p]
    if not self.vinil_dll.vinil_vhd_commit_structural_changes(self.vhd_pointer) == 1:
      raise VHDError("flush couldn't be executed")
      
  def __del__(self):
    if self.opened:
      self.close()
