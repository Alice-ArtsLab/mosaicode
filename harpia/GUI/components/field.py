from harpia.GUI.fieldtypes import *

class Field(object):

    def __init__(self, data, event):
        pass

    def get_type(self):
        return HARPIA_NONE

    def get_value(self):
        return 0
    
    def check_value(self, data, key, value):
        if key in data:
            return
        else:
            data[key] = value
