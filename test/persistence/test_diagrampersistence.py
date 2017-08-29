#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.persistence.diagrampersistence import DiagramPersistence

from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow

class TestDiagramPersistence(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.diagrampersistence = DiagramPersistence()

    # ----------------------------------------------------------------------x
    def test_load(self):

        diagram = Diagram(MainWindow())
        # NOTE: TESTANDO COM DIAGRAM = None
        # BUG: NÃO TRATA None
        # diagram = None
        # self.assertIsNone(self.diagrampersistence.load(diagram))

        # NOTE: TESTANDO COM NOME DE ARQUIVO VERDADEIRO
        diagram.file_name = "/home/lucas/mosaicode/teste/Untitled.mscd"
        self.assertTrue(self.diagrampersistence.load(diagram))

        # NOTE: TESTANDO COM NOME DE ARQUIVO INEXISTENTE
        # BUG: NÃO TRATA DIAGRAM INEXISTENTE
        # diagram.file_name = "/home/lucas/mosaicode/extensions/teste.py"
        # self.assertIsNone(self.diagrampersistence.load(diagram))

    # ----------------------------------------------------------------------x
    def test_save(self):
        # NÃO TRABALHA COM None
        # diagram = None
        # self.assertTrue(self.diagrampersistence.save(diagram))

        diagram = Diagram(MainWindow())
        self.assertTrue(self.diagrampersistence.save(diagram))

        diagram.file_name = "Template de teste"
        self.assertTrue(self.diagrampersistence.save(diagram))
