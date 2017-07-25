#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.components.commentfield import CommentField
# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.commentfield import CommentField

class TestCommentField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        data = {"label": ("Type"), "name":"type", "value": "text"}
        self.commentfield = CommentField(data, self)

    # ----------------------------------------------------------------------
    def test_get_value(self):
        self.assertTrue(self.commentfield.get_value())

    # ----------------------------------------------------------------------
    def test_set_value(self):
        value = "Teste"
        self.assertIsNone(self.commentfield.set_value(value))
        value = "Algo"
        self.assertIsNone(self.commentfield.set_value(value))
