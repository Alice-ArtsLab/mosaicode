#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.floatfield import FloatField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.floatfield import FloatField

class TestFloatField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
	data = 1
        self.floatfield = FloatField(data, self)
        data = {"label": ("Type"), "name":"type", "value": 13.05}
        self.floatfield = FloatField(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.floatfield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):

        value = -65590.0
        self.assertIsNone(self.floatfield.set_value(value))
        value = -65590
        self.assertIsNone(self.floatfield.set_value(value))
        value = 9223372036854775807
        self.assertIsNone(self.floatfield.set_value(value))
        value = 9223372036854775806
        self.assertIsNone(self.floatfield.set_value(value))
        value = 0
        self.assertIsNone(self.floatfield.set_value(value))
        value = 9223372036854775808
        self.assertIsNone(self.floatfield.set_value(value))
