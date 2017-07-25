#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.model.codetemplate import CodeTemplate


class TestCodeTemplateControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.codetemplate = CodeTemplate()
        self.codetemplatecontrol = CodeTemplateControl()

    # ----------------------------------------------------------------------
    def test_load(self):
        self.assertIsNone(self.codetemplatecontrol.load("test_codegenerator.py"))
        self.assertIsNone(self.codetemplatecontrol.load("Aa"))

    # ----------------------------------------------------------------------
    def test_export_xml(self):
        self.assertIsNone(self.codetemplatecontrol.export_xml())

    # ----------------------------------------------------------------------
    def test_export_python(self):
        self.assertIsNone(self.codetemplatecontrol.export_python())

    # ----------------------------------------------------------------------
    def test_add_code_template(self):
        self.assertIsNone(self.codetemplatecontrol.add_code_template(self.codetemplate))

    # ----------------------------------------------------------------------
    def test_delete_code_template(self):
        self.assertFalse(self.codetemplatecontrol.delete_code_template(self.codetemplate))

        self.codetemplate.type = "ts"
        self.codetemplate.name = "Teste"
        self.codetemplate.description = ""
        self.codetemplate.language = ""
        self.codetemplate.command = ""
        self.codetemplate.extension = ".xml"
        self.codetemplate.code = "Testando"
        self.codetemplate.source = "xml"

        # PARA QUE O TESTE ABAIXO SEJA EXECUTADO,
        # DEVE-SE CRIAR UM ARQUIVO c.xml DENTRO
        # DA PASTA mosaicode/extensions, QUE SE
        # ENCONTRA NA home do usuário. ASSIM,
        # O TESTE IRÁ ABRANGER 100% DA CLASSE.

        # LEMBRANDO QUE, ISTO É ERRADO, POIS NÃO
        # EXCLUIRÁ O PLUGIN EM SI, MAS, UM ARQUIVO
        # QUALQUER XML. CASO NÃO SE DELETE, NÃO APRESENTA
        # NENHUMA MENSAGEM DE ERRO.

        self.assertFalse(self.codetemplatecontrol.delete_code_template(self.codetemplate))


    # ----------------------------------------------------------------------
    def test_print_template(self):
        self.assertIsNone(self.codetemplatecontrol.print_template(self.codetemplate))
