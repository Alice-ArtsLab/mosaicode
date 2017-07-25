#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.combofield import ComboField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.combofield import ComboField

class TestComboField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type",
                "value": "Banana", "values":["Banana", "Apple", "Orange"]}
        self.combofield = ComboField(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.combofield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):
        value = "Teste"
        self.assertIsNone(self.combofield.set_value(value))
        value = "Algo"
        self.assertIsNone(self.combofield.set_value(value))
        value = "Banana"
        self.assertIsNone(self.combofield.set_value(value))
