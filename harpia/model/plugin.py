#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Plugin(object):
    """
    This class contains the base attributes of each plug-in,
    their position on the screen, id and others applicable properties for each one.
    """

    # ----------------------------------------------------------------------
    def __init__(self, plugin = None):

        self.id = -1
        self.x = 0
        self.y = 0

        self.type = self.__class__.__module__
        self.language = ""
        self.framework = ""
        self.source = "python"

        # Appearance
        self.help = ""
        self.label = ""
        self.color = "200:200:25:150"
        self.group = "Undefined"
        self.in_ports = []
        self.out_ports = []

        # Code generation
        self.properties = []
        self.codes = ["","","","",""] # Empty array with 5 positions

        self.header = ""
        self.vars = ""
        self.function_call = ""
        self.dealloc = ""
        self.out_dealloc = ""

        if plugin == None: return
        for key in plugin.__dict__:
            self.__dict__[key] = plugin.__dict__[key]

    # ----------------------------------------------------------------------
    def get_help(self):
        """
        Return the plugin help text.

            Returns:
                * **Types**: :class:`str<str>`
                The return value.
        """
        return self.help

    # ----------------------------------------------------------------------
    def get_label(self):
        """
        Return the plugin label.

        Returns:
            * **Types**: :class:`str<str>`
            The return value.
        """
        return self.label

    # ----------------------------------------------------------------------
    def get_icon(self):
        """
        Return the plugin icon path.

        Returns:
            * **Types**: :class:`str<str>`
            The return value is the icon path.
        """

        return self.icon

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
                color = [int(color[0:2],16),
                         int(color[4:6],16),
                         int(color[8:10],16)]
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
    def get_in_ports(self):
        """
        Return types of plugin entries.

        Returns:
            * **Types**: :class:`list<list>`
            The return is a list of types plugin entries.
        """
        return self.in_ports

    # ----------------------------------------------------------------------
    def get_out_ports(self):
        """
        Return types of plugin outputs.

        Returns:
            * **Types**: :class:`list<list>`
            The return is a list of types plugin outputs.
        """
        return self.out_ports

    # ----------------------------------------------------------------------
    def get_group(self):
        """
        Returns the group name that plugin belongs.

        Returns:
            * **Types**: :class:`str<str>`
            The return value.
        """
        return self.group

    # ----------------------------------------------------------------------
    def get_position(self):
        """
        Return the plugin position on the work area.

        Returns:
            * **Types**: :class:`int<int>` and :class:`int<int>`
            Returns the **x** and **y** position of the plugin
        """
        return (self.x, self.y)

    # ----------------------------------------------------------------------
    def get_type(self):
        """
        Return the plugin type.

        Returns:
            * **Types**: :class:`str<str>`
            The return value is the class module. Like:
                * *"harpia.plugins.c.opencv.xor"*
                * *"harpia.plugins.javascript.webaudio.addfloat"*
        """
        return self.type

    # ----------------------------------------------------------------------
    def set_id(self, value):
        """
        Set the plugin id.

        Parameters:
            * **value** (:class:`int<int>`): The plugin id number.
        """
        self.id = int(value)

    # ----------------------------------------------------------------------
    def get_id(self):
        """
        Return the plugin id.

        Returns:
            * **Types**: :class:`int<int>`
            The return value.
        """
        return int(self.id)

    # ----------------------------------------------------------------------
    def get_language(self):
        """
        Return the plugin programming language.

        Returns:
            * **Types**: :class:`str`<str>
            The return value.
        """

        try:
            return self.language
        except:
            return None

    # ----------------------------------------------------------------------
    def get_framework(self):
        """
        Return the plugin framework.

        Returns:
            * **Types**: :class:`str`<str>
            The return value.
        """

        try:
            return self.framework
        except:
            return None

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]
            else:
                print "Plugin.set_property (" + self.type + \
                        ") ERROR: key ", key, "not present"

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self.get_id())

# ------------------------------------------------------------------------------
