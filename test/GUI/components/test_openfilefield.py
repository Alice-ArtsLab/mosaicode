#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.openfilefield import OpenFileField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.openfilefield import OpenFileField

class TestOpenFileField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": "text.txt"}
        self.openfilefield = OpenFileField(data, self)


    # ----------------------------------------------------------------------
    def test_set_parent_window(self):
        self.assertIsNone(self.openfilefield.set_parent_window(None))

    # ----------------------------------------------------------------------
    def test_on_choose_file(self):
        self.assertIsNone(self.openfilefield.on_choose_file(None))

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.openfilefield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):
        value = ""
        self.assertIsNone(self.openfilefield.set_value(value))
        value = "255"
        self.assertIsNone(self.openfilefield.set_value(value))
        value = "234:233"
        self.assertIsNone(self.openfilefield.set_value(value))
        value = "12:233:12"
        self.assertIsNone(self.openfilefield.set_value(value))
        value = "TEST"
        self.assertIsNone(self.openfilefield.set_value(value))
        value = "./testando"
        self.assertIsNone(self.openfilefield.set_value(value))
