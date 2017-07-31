#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.dialog import Dialog
from mosaicode.GUI.mainwindow import MainWindow

class TestDialog(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.dialog = Dialog()

    # ----------------------------------------------------------------------x
    def test_open_dialog(self):

        # Deve-se apertar o botão CANCEL
        title = None
        main_window = None
        filetype = None
        self.assertIsNone(self.dialog.open_dialog(title, main_window, filetype))

        # Deve-se pesquisar um arquivo para abrir
        title = None
        main_window = MainWindow()
        filetype = "xml"
        self.assertIsNotNone(self.dialog.open_dialog(title, main_window, filetype))

        #title = None
        #main_window = None
        #filetype = None
        #self.assertIsNone(self.dialog.open_dialog(title, main_window, filetype))


    # ----------------------------------------------------------------------x
    def test_save_dialog(self):
        main_window = MainWindow()
        title = "Save"
        filetype = None
        self.assertIsNone(self.dialog.save_dialog(main_window, title, filetype))

        main_window = MainWindow()
        title = "Save"
        filetype = "XML"
        self.assertIsNone(self.dialog.save_dialog(main_window, title, filetype))


    # ----------------------------------------------------------------------x
    def test_confirm_overwrite(self):

        name = "/home/lucas/Faculdade/2017-1/Iniciacao/Mosaicode/mosaicode/test/files_for_test/output/Dialog_Overwrite.mscd"
        main_window = None
        self.assertTrue(self.dialog.confirm_overwrite(name, main_window))

        # Testando o botão CANCEL
        name = "/home/lucas/Faculdade/2017-1/Iniciacao/Mosaicode/mosaicode/test/files_for_test/input/Teste1.mscd"
        main_window = None
        self.assertFalse(self.dialog.confirm_overwrite(name, main_window))

        # Testando o botão OK
        name = "/home/lucas/Faculdade/2017-1/Iniciacao/Mosaicode/mosaicode/test/files_for_test/input/Teste1.mscd"
        main_window = None
        self.assertTrue(self.dialog.confirm_overwrite(name, main_window))

        name = ""
        main_window = MainWindow()
        self.assertTrue(self.dialog.confirm_overwrite(name, main_window))

        # NAO TRABALHA COM None
        #name = None
        #main_window = MainWindow()
        #self.assertTrue(self.dialog.confirm_overwrite(name, main_window))

    # ----------------------------------------------------------------------x
    def test_message_dialog(self):

        title = "Testando Message Dialog"
        message = "Realizando teste no message dialog"
        main_window = None
        self.assertIsNotNone(self.dialog.message_dialog(title, message, main_window))

        title = None
        message = None
        main_window = None
        self.assertIsNotNone(self.dialog.message_dialog(title, message, main_window))

    # ----------------------------------------------------------------------x
    def test_confirm_dialog(self):
        message = "Testando confirm dialog"
        main_window = None
        self.assertIsNotNone(self.dialog.confirm_dialog(message, main_window))
