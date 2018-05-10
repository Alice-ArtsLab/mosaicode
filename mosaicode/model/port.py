# -*- coding: utf-8 -*-


class Port(object):
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

    """
    This class contains the base attributes of each block port.
    """
    INPUT = "input"
    OUTPUT = "output"

    # ----------------------------------------------------------------------
    def __init__(self):

        # Attributes defined by the Ports
        self.type = self.__class__.__module__
        self.language = ""
        self.hint = ""
        self.color = "#000"
        self.multiple = False
        self.file = None
        self.code = ""
        self.var_name = "$block[label]$_$block[id]$_$port[name]$"
        # Attributes defined in Block Ports
        self.conn_type = None
        self.name = None
        self.label = None
        self.index = -1
        self.type_index = -1

    # ----------------------------------------------------------------------
    def is_input(self):
        if self.conn_type == Port.INPUT:
            return True
        if self.conn_type == Port.OUTPUT:
            return False
        return False
# ------------------------------------------------------------------------------
