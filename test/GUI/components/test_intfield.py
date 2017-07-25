#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.intfield import IntField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.intfield import IntField

class TestIntField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": 13}
        self.intfield = IntField(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.intfield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):

        value = -65590
        self.assertIsNone(self.intfield.set_value(value))
        value = 65590
        self.assertIsNone(self.intfield.set_value(value))
        value = 6.5
        self.assertIsNone(self.intfield.set_value(value))
        value = 9223372036854775807
        self.assertIsNone(self.intfield.set_value(value))
        value = 0
        self.assertIsNone(self.intfield.set_value(value))
        value = 9223372036854775808
        self.assertIsNone(self.intfield.set_value(value))
