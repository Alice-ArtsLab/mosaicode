#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.persistence.blockpersistence import BlockPersistence

from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel


class TestBlockPersistence(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.blockpersistence = BlockPersistence()

    # ----------------------------------------------------------------------x
    def test_load(self):

        # TESTANDO COM NOME DE ARQUIVO = None
        file_name = ""
        self.assertIsNone(self.blockpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO INEXISTENTE
        file_name = "/home/lucas/mosaicode/extensions/teste.py"
        self.assertIsNone(self.blockpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO FALSO (INCOMPATÍVEL)
        file_name = "/home/lucas/mosaicode/extensions/a.py"
        self.assertIsNone(self.blockpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO VERDADEIRO
        file_name = "/home/lucas/mosaicode/extensions/mosaicode.model.blockmodel.xml"
        self.assertIsNone(self.blockpersistence.load(file_name))

        # TESTANDO COM NOME DE ARQUIVO VERDADEIRO MAS COM RETORNO
        file_name = "/home/lucas/mosaicode/extensions/mosaicode.model.blockmodel_teste.xml"
        self.assertIsNotNone(self.blockpersistence.load(file_name))

    # ----------------------------------------------------------------------x
    def test_save(self):
        # NÃO TRABALHA COM None
        # block = None
        # self.assertTrue(self.blockpersistence.save(block))

        diagram = Diagram(MainWindow())
        block = Block(diagram, None)
        self.assertTrue(self.blockpersistence.save(block))

        diagram = Diagram(MainWindow())
        blockmodel = BlockModel(None)
        block = Block(diagram, blockmodel)
        block.type = "teste_blockpersistence"
        self.assertTrue(self.blockpersistence.save(block))


    # ----------------------------------------------------------------------x
    def test_save_python(self):

        # NÃO TRABALHA COM None
        # block = None
        # self.assertFalse(self.blockpersistence.save_python(block))

        diagram = Diagram(MainWindow())
        block = Block(diagram, None)
        self.assertTrue(self.blockpersistence.save_python(block))

        diagram = Diagram(MainWindow())
        blockmodel = BlockModel(None)
        block = Block(diagram, blockmodel)
        block.type = "teste_blockpersistence"
        self.assertTrue(self.blockpersistence.save_python(block))
