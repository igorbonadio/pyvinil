import unittest

from ctypes import *

from pyvinil.vhd import VHD

class TestVHD(unittest.TestCase):
  
  def test_open(self):
    vhd_files = ["vhd_test_y.vhd", "vhd_test_zero.vhd"]
    for vhd_path in vhd_files:
      vhd = None
      try:
        vhd = VHD.open("pyvinil/test/data/" + vhd_path)
        vhd.close()
      except:
        self.assertTrue(False, "Cannot open " + vhd_path)
  
  def test_read(self):
    vhd_files = ["vhd_test_y.vhd", "vhd_test_zero.vhd"]
    for vhd_path in vhd_files:
      vhd = None
      try:
        vhd = VHD.open("pyvinil/test/data/" + vhd_path)
      except:
        self.assertTrue(False, "Cannot open " + vhd_path)
      try:
        sector = vhd.read(1)
      except:
        self.assertTrue(False, "Cannot read 1 sector from " + vhd_path)
      vhd.close()
  
  def test_write(self):
    vhd_files = ["vhd_test_y.vhd", "vhd_test_zero.vhd"]
    for vhd_path in vhd_files:
      vhd = None
      try:
        vhd = VHD.open("pyvinil/test/data/" + vhd_path)
      except:
        self.assertTrue(False, "Cannot open " + vhd_path)
      try:
        vhd.seek(3, 1)
      except:
        self.assertTrue(False, "Cannot call seek to " + vhd_path)
      try:
        buf = 'a'*512
        vhd.write(buf, 1)
      except:
        self.assertTrue(False, "Cannot write 1 sector to " + vhd_path)
      try:
        self.assertEqual(vhd.tell(), 4, "Tell returns a wrong sector")
      except:
        self.assertTrue(False, "Cannot call seek to " + vhd_path)
      vhd.close()
      
  def test_footer(self):
    vhd_files = ["vhd_test_y.vhd", "vhd_test_zero.vhd"]
    for vhd_path in vhd_files:
      vhd = None
      try:
        vhd = VHD.open("pyvinil/test/data/" + vhd_path)
      except:
        self.assertTrue(False, "Cannot open " + vhd_path)
      self.assertTrue(vhd.footer is not None, "Cannot access " + vhd_path + "'s footer")
      self.assertEqual(vhd.footer.cookie, "conectix", "Invalid cookie")
      vhd.footer.disk_type = 3
      try:
        vhd.commit_structural_changes()
      except:
        self.assertTrue(False, "Cannot commit structural changes of " + vhd_path)
      vhd.close()

def suite():
  return unittest.TestLoader().loadTestsFromTestCase(TestVHD)
