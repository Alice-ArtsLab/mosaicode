#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mosaicode.GUI.fieldtypes import *

class CommentModel(object):
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
    """
    This class contains the base attributes of each block,
    their position on the screen, id and others applicable properties for
    each one.
    """

    # ----------------------------------------------------------------------
    def __init__(self, comment=None):

        self.id = -1
        self.x = 0
        self.y = 0
        self.properties = [
                {"label": "Text",
                "name": "text",
                "value": "Comment",
                "type": MOSAICODE_COMMENT,
                }]

        if comment is None:
            return

        # If block is defined, copy everything and load it!
        for key in self.__dict__:
            self.__dict__[key] = comment.__dict__[key]

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        if data is None:
            return
        if self.get_properties() is None:
            self.properties = []
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def __str__(self):
        if self.properties is None:
            self.properties = []
        if len(self.properties) < 1:
            return ""
        if "value" in self.properties[0]:
            return str(self.properties[0]["value"])
        else:
            return ""

# ------------------------------------------------------------------------------
