#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the PreferenceWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.combofield import ComboField

import gettext

_ = gettext.gettext


class SelectCodeTemplate(Gtk.Dialog):
    """
    This class contains methods related the PreferenceWindow class
    """

    def __init__(self, main_window, template_list):
        """
        This method is the constructor.
        """
        Gtk.Dialog.__init__(self, _("Select Code Template"), main_window,
                            0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.template_list = template_list

        templates = []
        for code_template in template_list:
            templates.append(code_template.description)

        data = {"label": _("Code Template"), "name":"template", "values": templates}
        self.field = ComboField(data, None)
        self.field.field.set_active(0)
        self.get_content_area().add(self.field)

    # ----------------------------------------------------------------------
    def get_value(self):
        self.show_all()
        response = self.run()
        index = self.field.field.get_active()
        template = self.template_list[index]
        self.close()
        self.destroy()
        return self.template_list[index]
