"""
This module contains the Field class.
"""
class Field(object):
    """
    This class contains methods related the Field class.
    """

    configuration = {}
    # ----------------------------------------------------------------------

    def __init__(self, data, event):
        """
        This method is the constructor.
        """
        self.data = data

    # ----------------------------------------------------------------------
    def get_type(self):
        from harpia.GUI.fieldtypes import *
        return HARPIA_NONE

    # ----------------------------------------------------------------------
    @classmethod
    def get_configuration(cls):
        return cls.configuration

    # ----------------------------------------------------------------------
    def get_value(self):
        return 0

    # ----------------------------------------------------------------------
    def set_value(self, value):
        pass

    # ----------------------------------------------------------------------
    def check_values(self):
        for key in self.get_configuration():
            if key in self.data:
                continue
            else:
                self.data[key] = self.get_configuration()[key]
