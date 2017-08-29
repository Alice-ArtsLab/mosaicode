#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence

from mosaicode.model.codetemplate import CodeTemplate

class TestCodeTemplatePersistence(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.codetemplatepersistence = CodeTemplatePersistence()

    # ----------------------------------------------------------------------x
    def test_load(self):

        # TESTANDO COM NOME DE ARQUIVO = None
        file_name = ""
        self.assertIsNone(self.codetemplatepersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO INEXISTENTE
        file_name = "/home/lucas/mosaicode/extensions/teste.py"
        self.assertIsNone(self.codetemplatepersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO FALSO (INCOMPATÍVEL)
        file_name = "/home/lucas/mosaicode/extensions/a.py"
        self.assertIsNone(self.codetemplatepersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO VERDADEIRO
        file_name = "/home/lucas/mosaicode/extensions/mosaicode.model.codetemplate.xml"
        self.assertIsNone(self.codetemplatepersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO VERDADEIRO MAS COM RETORNO
        file_name = "/home/lucas/mosaicode/extensions/mosaicode.model.codetemplate_teste.xml"
        self.assertIsNone(self.codetemplatepersistence.load(file_name))

    # ----------------------------------------------------------------------x
    def test_save(self):
        # NÃO TRABALHA COM None
        # code_template = None
        # self.assertTrue(self.codetemplatepersistence.save(code_template))


        code_template = CodeTemplate()
        self.assertTrue(self.codetemplatepersistence.save(code_template))

        code_template.name = "Template de teste"
        self.assertTrue(self.codetemplatepersistence.save(code_template))


    # ----------------------------------------------------------------------x
    def test_save_python(self):

        # NÃO TRABALHA COM None
        # code_template = None
        # self.assertFalse(self.codetemplatepersistence.save_python(code_template))

        code_template = CodeTemplate()
        self.assertTrue(self.codetemplatepersistence.save_python(code_template))

        code_template.name = "Template de teste"
        self.assertTrue(self.codetemplatepersistence.save_python(code_template))
