#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ExtensionsManagerControl class.
"""

from mosaicode.control.maincontrol import *
from mosaicode.system import *
from mosaicode.control.portcontrol import PortControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.GUI.dialog import Dialog
from mosaicode.plugins.extensionsmanager.GUI.blockcodeeditor import BlockCodeEditor
from mosaicode.plugins.extensionsmanager.GUI.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.GUI.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.GUI.codetemplateeditor import CodeTemplateEditor
from mosaicode.plugins.extensionsmanager.GUI.codetemplatemanager import CodeTemplateManager
from mosaicode.plugins.extensionsmanager.GUI.porteditor import PortEditor
from mosaicode.plugins.extensionsmanager.GUI.portmanager import PortManager

import gettext
_ = gettext.gettext

class ExtensionsManagerControl(object):
    """
    This class contains methods related the ExtensionsManagerControl.
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        """Constructor."""
        self.main_window = main_window

    # ----------------------------------------------------------------------
    def code_template_manager(self):
        """
        This add a new Code Template.
        """
        CodeTemplateManager(self.main_window)

    # ----------------------------------------------------------------------
    def block_manager(self):
        """
        This add a new Block.
        """
        BlockManager(self.main_window)

    # ----------------------------------------------------------------------
    def port_manager(self):
        """
        This add a new port.
        """
        PortManager(self.main_window)

    # ----------------------------------------------------------------------
    @classmethod
    def export_extensions(cls):
        self.export_xml()

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        System()
        BlockControl.export_xml()
        PortControl.export_xml()
        CodeTemplateControl.export_xml()

    # ----------------------------------------------------------------------
    def export_xml_dialog(self):
        self.export_xml()
        Dialog().message_dialog("Exporting as xml", "Exported successfully!", self.main_window)

# ----------------------------------------------------------------------
