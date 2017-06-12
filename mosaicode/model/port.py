# -*- coding: utf-8 -*-

class Port(object):
    """
    This class contains the base attributes of each plugin port.
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
        self.input_codes = ["","","","",""]
        self.output_codes = ["","","","",""]
        self.var_name = "block_$id$_$conn_type$$port_number$"

# ------------------------------------------------------------------------------
