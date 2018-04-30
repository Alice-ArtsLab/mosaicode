#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CommentModel(object):
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
    """
    This class contains the base attributes of each block,
    their position on the screen, id and others applicable properties for
    each one.
    """

    # ----------------------------------------------------------------------
    def __init__(self):

        self.id = -1
        self.x = 0
        self.y = 0

        self.text = ""

    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self.text)

# ------------------------------------------------------------------------------
