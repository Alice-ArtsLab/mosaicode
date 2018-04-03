#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the BlockProperties.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from propertybox import PropertyBox
import gettext
_ = gettext.gettext


class BlockProperties(Gtk.Notebook):
    """
    This class contains the methods related to BlockProperties class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        """
        This method is the constuctor.

            Parameters:
                main_window
        """
        Gtk.Notebook.__init__(self)
        self.main_window = main_window

        # Properties tab
        properties_scrolled_window = Gtk.ScrolledWindow()
        properties_scrolled_window.set_border_width(10)
        properties_scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.property_box = PropertyBox(self.main_window)
        properties_scrolled_window.add(self.property_box)
        self.append_page(
            properties_scrolled_window, Gtk.Label(_("Properties")))

        # Help tab
        help_scrolled_window = Gtk.ScrolledWindow()
        help_scrolled_window.set_border_width(10)
        help_scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.help = Gtk.TextView()
        self.help.set_wrap_mode(Gtk.WrapMode.WORD)
        self.help.set_editable(False)
        self.help.set_left_margin(2)
        help_scrolled_window.add(self.help)
        self.append_page(help_scrolled_window, Gtk.Label(_("Help")))
        self.set_properties(None)

# ----------------------------------------------------------------------
    def set_block(self, block):
        """
        This method set properties of each block.

            Parameters:
            * **block** (:class:`block<mosaicode.GUI.block>`)
        """
        self.help.get_buffer().set_text(block.help)
        self.property_box.set_block(block)

# ----------------------------------------------------------------------
    def set_comment(self, comment):
        """
        This method set properties of each comment.

            Parameters:
            * **comment** (:class:`block<mosaicode.GUI.comment>`)
        """
        self.property_box.set_comment(comment)

# ----------------------------------------------------------------------
