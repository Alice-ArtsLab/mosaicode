#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.field import Field
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.field import Field

class TestField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": "Test"}
        self.field = Field(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        value = self.field.get_value()
        assert value == 0

    # ----------------------------------------------------------------------
    def test_set_value(self):
        value = "Atenção"
        self.assertFalse(self.field.set_value(value))

    # ----------------------------------------------------------------------
    def test_check_values(self):
        self.assertFalse(self.field.check_values())
        self.data = {"label": "", "name": "", "value": ""}
        self.assertFalse(self.field.check_values())
        self.data = {}
        self.assertFalse(self.field.check_values())
