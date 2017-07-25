#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.colorfield import ColorField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.colorfield import ColorField

class TestColorField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": "255:255:255:255"}
        self.colorfield = ColorField(data, self)

    # ----------------------------------------------------------------------
    def test_set_parent_window(self):
        self.assertIsNone(self.colorfield.set_parent_window(None))

    # ----------------------------------------------------------------------
    def test_on_choose_color(self):
        self.assertIsNone(self.colorfield.on_choose_color(None))

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.colorfield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):
        value = "#FFFFFF"
        self.assertIsNone(self.colorfield.set_value(value))
        value = "255"
        self.assertIsNone(self.colorfield.set_value(value))
        value = "234:233"
        self.assertIsNone(self.colorfield.set_value(value))
        value = "12:233:12"
        self.assertIsNone(self.colorfield.set_value(value))
        value = 22
        self.assertIsNone(self.colorfield.set_value(value))
        value = ""
        self.assertIsNone(self.colorfield.set_value(value))
