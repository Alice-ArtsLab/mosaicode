#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.codetemplatemanager import CodeTemplateManager

from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.codetemplate import CodeTemplate

class TestCodeTemplateManager(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.codetemplatemanager = CodeTemplateManager(win)

    # ----------------------------------------------------------------------x
    def test_add_code_template(self):
        code_template = CodeTemplate()
        self.assertIsNone(self.codetemplatemanager.add_code_template(code_template))

        code_template.type = "Language Test"
        code_template.name = "Testando Code Template"
        code_template.description = "Um teste para code template em Add Code Template"
        code_template.language = ""
        code_template.command = ""
        code_template.extension = "teste"
        code_template.code = "Testando 1 2 3"
        code_template.source = "python"
        self.assertIsNone(self.codetemplatemanager.add_code_template(code_template))

        # NAO ACEITA NONE
        # code_template.type = None
        # code_template.name = None
        # code_template.description = None
        # code_template.language = None
        # code_template.command = None
        # code_template.extension = None
        # code_template.code = None
        # code_template.source = None
        # self.assertIsNone(self.codetemplatemanager.add_code_template(code_template))
