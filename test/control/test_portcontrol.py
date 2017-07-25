#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.control.portcontrol import PortControl
from mosaicode.model.port import Port

class TestMainControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.port_control = PortControl()
        self.port = Port()

    # ----------------------------------------------------------------------
    def test_load(self):
        file_name = "TESTE"
        self.assertIsNone(self.port_control.load(file_name))
        file_name = "AAA.xml"
        self.assertIsNone(self.port_control.load(file_name))

    # ----------------------------------------------------------------------
    def test_export_xml(self):
        self.assertIsNone(self.port_control.export_xml())

    # ----------------------------------------------------------------------
    def test_export_python(self):
        self.assertIsNone(self.port_control.export_python())

    # ----------------------------------------------------------------------
    def test_print_port(self):

        #port = Port()

        #port.type = "c"
        #port.language = "c"
        #port.source = "xml"
        #port.code = "xxxx"

        self.assertIsNone(self.port_control.print_port(self.port))

    # ----------------------------------------------------------------------
    def test_add_port(self):

        #port = Port()

        #port.type = "c"
        #port.language = "c"
        #port.source = "xml"
        #port.code = "xxxx"

        self.assertIsNone(self.port_control.add_port(self.port))

    # ----------------------------------------------------------------------
    def test_delete_port(self):

        self.assertIsNone(self.port_control.delete_port(self.port))
