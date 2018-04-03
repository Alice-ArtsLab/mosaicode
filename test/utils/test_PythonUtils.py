#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.utils.PythonUtils import PythonParser

class TestPythonParser(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        file_name = "Teste"
        self.python_parser = PythonParser(file_name)
        file_name = None
        self.python_parser = PythonParser(file_name)

    # ----------------------------------------------------------------------
    def test_setAttribute(self):
        self.assertIsNone(self.python_parser.setAttribute(self.python_parser.class_name, 10))

    # ----------------------------------------------------------------------
    def test_getAttributeValue(self):
        self.assertIsNone(self.python_parser.getAttributeValue(self.python_parser.class_name))
        teste = None
        self.assertIsNone(self.python_parser.getAttributeValue(teste))

    # ----------------------------------------------------------------------
    def test_getDependencies(self):
        self.assertIsNotNone(self.python_parser.getDependencies())

    # ----------------------------------------------------------------------
    def test_getInheritedClasses(self):
        self.assertIsNotNone(self.python_parser.getInheritedClasses())

    # ----------------------------------------------------------------------
    def test_clear_string(self):
        string = '\n'
        self.assertIsNotNone(self.python_parser.clear_string(string))
        string = ' '
        self.assertIsNotNone(self.python_parser.clear_string(string))
        string = "TESTE_TESTES TESTE"
        self.assertIsNotNone(self.python_parser.clear_string(string))

    # ----------------------------------------------------------------------
    def test_save(self):
        file_name = "Testando.txt"
        self.python_parser.class_name = "Testando_save"
        self.assertIsNone(self.python_parser.save(file_name))
