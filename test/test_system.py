#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.system import System


class Log(object):

    def log(self, msg):
        print msg.encode('ascii', 'ignore')


class TestSystem(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        System()
        self.log = Log()

    def test_set_log(self):
        self.assertIsNone(System.set_log(self.log.log("A")))
        #System.set_log(Log())

    def test_log(self):
        self.assertIsNone(System.log(self.log.log("as")))
        #self.assertIsNone(self.system.log("Hello World"))
        #System.log("Hello World")

    def test_get_user_dir(self):

        path = "/home/lucas/mosaicode"
        self.assertEqual(path, System.get_user_dir(), 'Pasta de usuário não encontrada')
        path = "/usr/share/mosaicode/"
        self.assertNotEqual(path, System.get_user_dir(), 'Pasta de usuário não encontrada')

        #self.assertIsNotNone(System.get_user_dir(), 'message')
        #System.get_user_dir()
