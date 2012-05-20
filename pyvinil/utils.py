import platform
from ctypes import *

def singleton(cls):
    instance_list = list()
    def getinstance():
        if not len(instance_list):
            instance_list.append(cls())
        return instance_list[0]
    return getinstance

@singleton
class VinilDynamicLibrary:
  def __init__(self):
    self.dll = cdll.LoadLibrary("libvinil.dylib")
    
  def get_dl_path(self):
    if platform.system() == "Linux":
      return "libvinil.so"
    elif platform.system() == "Windows":
      return "vinil.dll"
    else: # MacOS X
      return "libvinil.dylib"
    
  def get_dynamic_library(self):
    return self.dll


def uuid_generate():
  vinil_dll = VinilDynamicLibrary().get_dynamic_library()
  vinil_dll.vinil_uuid_generate.argtypes = [c_void_p]
  uuid = (c_char*16)()
  vinil_dll.vinil_uuid_generate(byref(uuid))
  return uuid.value