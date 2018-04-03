#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.persistence.portpersistence import PortPersistence

from mosaicode.model.port import Port


class TestPortPersistence(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.portpersistence = PortPersistence()

    # ----------------------------------------------------------------------x
    def test_load(self):

        # TESTANDO COM NOME DE ARQUIVO = None
        file_name = ""
        self.assertIsNone(self.portpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO INEXISTENTE
        file_name = "/home/lucas/mosaicode/extensions/teste.py"
        self.assertIsNone(self.portpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO FALSO (INCOMPATÍVEL)
        file_name = "/home/lucas/mosaicode/extensions/a.py"
        self.assertIsNone(self.portpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO FALSO DE XML
        file_name = "/home/lucas/mosaicode/extensions/mosaicode.model.portmodel.xml"
        self.assertIsNone(self.portpersistence.load(file_name))

        # TESTANDO COM ARQUIVO COM port.type = ""
        file_name = "/home/lucas/mosaicode/extensions/mosaicode.model.port_teste.xml"
        self.assertIsNone(self.portpersistence.load(file_name))


        # TESTANDO COM NOME DE ARQUIVO VERDADEIRO
        file_name = "/home/lucas/mosaicode/extensions/ports/mosaicode.model.port.xml"
        self.assertIsNotNone(self.portpersistence.load(file_name))

    # ----------------------------------------------------------------------x
    def test_save(self):

        port = Port()
        self.assertTrue(self.portpersistence.save(port))

        port.type = "teste_portpersistence"
        self.assertTrue(self.portpersistence.save(port))

        # NÃO TRABALHA COM None
        # port = None
        # self.assertFalse(self.portpersistence.save(port))

    # ----------------------------------------------------------------------x
    def test_save_python(self):

        port = Port()
        self.assertTrue(self.portpersistence.save_python(port))

        port.type = "teste_portpersistence"
        self.assertTrue(self.portpersistence.save_python(port))

        # NÃO TRABALHA COM None
        # port = None
        # self.assertFalse(self.portpersistence.save_python(port))
