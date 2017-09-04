# -*- coding: utf-8 -*-

class Port(object):
    """
    This class contains the base attributes of each block port.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.type = self.__class__.__module__
        self.language = ""
        self.label = ""
        self.color = "#000"
        self.multiple = False
        self.source = "Python"
        self.code = ""
        self.var_name = "$id$_$output_port$$port_number$"

# ------------------------------------------------------------------------------
