#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.iconfield import IconField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.iconfield import IconField

class TestIconField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": 13.05}
        self.iconfield = IconField(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.iconfield.get_value())
        #pass

    # ----------------------------------------------------------------------
    def test_set_value(self):

        value = -65590.0
        self.assertIsNone(self.iconfield.set_value(value))
        value = -65590
        self.assertIsNone(self.iconfield.set_value(value))
        value = 9223372036854775807
        self.assertIsNone(self.iconfield.set_value(value))
        value = 9223372036854775806
        self.assertIsNone(self.iconfield.set_value(value))
        value = 0
        self.assertIsNone(self.iconfield.set_value(value))
        value = 9223372036854775808
        self.assertIsNone(self.iconfield.set_value(value))
