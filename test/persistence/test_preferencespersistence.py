#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.persistence.preferencespersistence import PreferencesPersistence

from mosaicode.model.preferences import Preferences


class TestPreferencesPersistence(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.preferencespersistence = PreferencesPersistence()

    # ----------------------------------------------------------------------x
    def test_load(self):
        self.assertIsNotNone(self.preferencespersistence.load())

    # ----------------------------------------------------------------------x
    def test_save(self):

        preferences = Preferences()
        self.assertTrue(self.preferencespersistence.save(preferences))

        preferences.type = "teste_preferencespersistence"
        self.assertTrue(self.preferencespersistence.save(preferences))

        # NÃO TRABALHA COM None
        # preferences = None
        # self.assertFalse(self.preferencespersistence.save(preferences))
