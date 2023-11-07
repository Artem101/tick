import ctypes
def foto(new_file):

 ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, new_file, 0x0001)
