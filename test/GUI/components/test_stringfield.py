#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.stringfield import StringField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.stringfield import StringField

class TestStringField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": "text"}
        self.stringfield = StringField(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.stringfield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):

        value = "-65590"
        self.assertIsNone(self.stringfield.set_value(value))
        value = ""
        self.assertIsNone(self.stringfield.set_value(value))
        value = "Tests"
        self.assertIsNone(self.stringfield.set_value(value))
        value = "aaaaa"
        self.assertIsNone(self.stringfield.set_value(value))
