#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.model.diagrammodel import DiagramModel


class TestDiagramModel(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.diagram_model = DiagramModel()

    # ----------------------------------------------------------------------
    # def test_patch_name(self):
    #
    #     # TESTANDO COM NOME DO ARQUIVO = None
    #     # NOTE: ERRO: str is not callable
    #     #self.diagram_model.file_name = ""
    #     #self.assertIsNotNone(self.diagram_model.patch_name())
    #
    #     self.diagram_model.file_name = "/home/lucas/Faculdade/2017-1/Iniciacao/Mosaicode/mosaicode/test/files_for_test/input/And.mscd"
    #     self.assertIsNone(self.diagram_model.patch_name())
