#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BlockModel(object):
    """
    This class contains the base attributes of each block,
    their position on the screen, id and others applicable properties for
    each one.
    """

    # ----------------------------------------------------------------------
    def __init__(self, block=None):

        self.id = -1
        self.x = 0
        self.y = 0
        self.is_collapsed = False

        self.type = self.__class__.__module__
        self.language = ""
        self.framework = ""
        self.file = None

        # Appearance
        self.help = ""
        self.label = "A"
        self.color = "200:200:25:150"
        self.group = "Undefined"
        self.ports = []

        # Code generation
        self.properties = []
        self.codes = {}
        self.gen_codes = {}

        # Attributes to code generation
        self.weight = 0
        self.connections = []

        if block is None:
            return

        # If block is defined, copy everything and load it!
        for key in block.__dict__:
            self.__dict__[key] = block.__dict__[key]

    # ----------------------------------------------------------------------
    def get_color(self):
        """
        Get the color in RGB format and return in hexadecimal.

        Returns:
            * **Types**: :class:`str<str>`
            The return is the hex value reference to color. The hex value is a **str** type.
        """

        if self.color.startswith("#"):
            color = self.color.replace("#", "")
            if len(color) == 12: # RGB
                color = [int(color[0:2], 16),
                         int(color[4:6], 16),
                         int(color[8:10], 16)]
                color = int(color[0]) * 0x1000000 + \
                        int(color[1]) * 0x10000 + \
                        int(color[2]) * 0x100 + \
                        150 * 0x01 # Transparency
                return color

        if ":" in self.color:
            color = self.color.split(":")
            color = [int(color[0]), int(color[1]), int(color[2]), int(color[3])]
            color = int(color[0]) * 0x1000000 + \
                    int(color[1]) * 0x10000 + \
                    int(color[2]) * 0x100 + \
                    int(color[3]) * 0x01
            return color
        return 0

    # ----------------------------------------------------------------------
    def get_color_as_rgba(self):
        """
        Returns the color in RGBA format.

        Returns:
            * **Types**: :class:`str<str>`
            The return is the RGBA color. The hex value is a **str** type.
        """

        if self.color.startswith("#"):
            return self.color
        return "rgba(" + self.color.replace(":", ",") + ")"

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]
            else:
                from mosaicode.system import System as System
                System.log("BlockModel.set_property (" + self.type + \
                        ") ERROR: key " +  key + " not present")

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------------------
