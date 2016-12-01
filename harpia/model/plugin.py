#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Plugin(object):
    """
    This class contains the base attributes of each plug-in,
    their position on the screen, id and others applicable properties for each one.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.type = self.__class__.__module__
        self.language = ""
        self.framework = ""
        self.id = -1
        self.x = 0
        self.y = 0

        # Code generation
        self.properties = []
        self.header = ""
        self.vars = ""
        self.function_call = ""
        self.dealloc = ""
        self.out_dealloc = ""

        # Appearance
        self.help = ""
        self.label = ""
        self.icon = "images/show.png"
        self.color = "200:200:25:150"
        self.in_types = []
        self.out_types = []
        self.group = "Undefined"

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

        color = self.color.split(":")
        color = [int(color[0]), int(color[1]), int(color[2]), int(color[3])]
        color = int(color[0]) * 0x1000000 + \
            int(color[1]) * 0x10000 + \
            int(color[2]) * 0x100 + \
            int(color[3]) * 0x01
        return color

    # ----------------------------------------------------------------------
    def get_in_types(self):
        """
        Return types of plugin entries.

        Returns:
            * **Types**: :class:`list<list>`
            The return is a list of types plugin entries.
        """
        return self.in_types

    # ----------------------------------------------------------------------
    def get_out_types(self):
        """
        Return types of plugin outputs.

        Returns:
            * **Types**: :class:`list<list>`
            The return is a list of types plugin outputs.
        """
        return self.out_types

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
    def get_output_port_name(self, number):
        """
        Returns output port name
        Parameters:
            * **number** (:class:`int<int>`): The output port number
        Returns:
            * **Types**: :class:`str<str>`
            The return value.
        """
        return "block_" + str(self.id) + "o" + str(number)

    # ----------------------------------------------------------------------
    def get_input_port_name(self, number):
        """
        Returns input port name
        Parameters:
            * **number** (:class:`int<int>`): The input port number
        Returns:
            * **Types**: :class:`str<str>`
            The return value.
        """
        return "block_" + str(self.id) + "i" + str(number)

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
                * *"harpia.plugins.C.openCV.xor"*
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
        self.id = value

    # ----------------------------------------------------------------------
    def get_id(self):
        """
        Return the plugin id.

        Returns:
            * **Types**: :class:`int<int>`
            The return value.
        """
        return self.id

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
    def generate_header(self):
        return self.header

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return self.out_dealloc

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]
            else:
                print "Plugin.set_property ERROR: key ", key, "not present"

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def get_plugin(self):
        return self

    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self.get_id())

# ------------------------------------------------------------------------------
