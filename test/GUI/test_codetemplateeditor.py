#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.codetemplateeditor import CodeTemplateEditor

from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.codetemplatemanager import CodeTemplateManager

class TestCodeTemplateEditor(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow
        code_template_manager = CodeTemplateManager(win)
        code_template_name = "Teste"
        self.codetemplateeditor = CodeTemplateEditor(code_template_manager, code_template_name)
