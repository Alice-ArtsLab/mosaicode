#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.connector import Connector

from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.block import Block

class TestConnector(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        diagram = Diagram(win)

        blockmodel = BlockModel()
        source = Block(diagram, blockmodel)

        # NAO TRATA NONE
        # source = None
        source_port = 0
        conn_type = None
        self.connector = Connector(diagram, source, source_port, conn_type)

    # ----------------------------------------------------------------------x
    def test_delete(self):
        self.assertIsNone(self.connector.delete())

    # ----------------------------------------------------------------------x
    def test_update_tracking(self):
        newEnd = None
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [0, 0]
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [1, 1]
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [2, 1]
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [1, 2]
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [2, 2]
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [70, 70]
        self.assertIsNone(self.connector.update_tracking(newEnd))
        newEnd = [190, 70]
        self.assertIsNone(self.connector.update_tracking(newEnd))


    # ----------------------------------------------------------------------x
    def test_update_flow(self):
        # NOTE: NAO TRATA NONE. SE INICIALIZAR CONNECTOR,
        # QUE INICIALIZARA CONNECTORMODEL, O ATRIBUTO
        # SINK SERA NONE. E, COM ISSO, RESULTARA EM
        # ERRO. E SINK E DO TIPO BLOCK, ALGO DIFICIL
        # DE SER INICIALIZADO POR MEIO DE TESTE.
        self.assertIsNone(self.connector.update_flow())
