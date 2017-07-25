#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.control.maincontrol import MainControl
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class TestMainControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------
    def test_new(self):
        self.assertIsNone(self.main_control.new())

    # ----------------------------------------------------------------------
    def test_select_open(self):
        self.assertIsNone(self.main_control.select_open())

    # ----------------------------------------------------------------------
    def test_open(self):
        file_name = "app_data/examples/And.hrp"
        self.assertIsNone(self.main_control.open(file_name))
        file_name = "app_data/teste/And.mscd"
        self.assertIsNone(self.main_control.open(file_name))
        file_name = "app_data/teste/Outro.mscd"
        self.assertIsNone(self.main_control.open(file_name))
        file_name = "app_data/testando"
        self.assertIsNone(self.main_control.open(file_name))
        file_name = "app_data/testando/"
        self.assertIsNone(self.main_control.open(file_name))
        file_name = "app_data/testando/testando.mscd"
        self.assertIsNone(self.main_control.open(file_name))

    # ----------------------------------------------------------------------
    def test_close(self):
        self.assertIsNotNone(self.main_control.close())

    # ----------------------------------------------------------------------
    def test_save(self):
        save_as = False
        self.assertIsNone(self.main_control.save(save_as))
        save_as = True
        self.assertIsNone(self.main_control.save(save_as))

    # ----------------------------------------------------------------------
    def test_save_as(self):
        self.assertIsNone(self.main_control.save_as())

    # ----------------------------------------------------------------------
    #def test_rename_tab(self):
    #    self.main_control.rename_tab()

    # ----------------------------------------------------------------------
    def test_export_diagram(self):
        self.assertIsNone(self.main_control.export_diagram())

    # ----------------------------------------------------------------------
    def test_exit(self):
        widget1 = None
        data1 = None
        self.assertIsNone(self.main_control.exit(widget1, data1))

        #widget1 = O QUE E ESSE WIDGET?
        #data1 = O QUE E ESSE DATA?
        #self.assertTrue(self.main_control.exit(widget1, data))

    # ----------------------------------------------------------------------
    def test_select_all(self):
        self.assertIsNone(self.main_control.select_all())

    # ----------------------------------------------------------------------
    def test_cut(self):
        self.assertIsNone(self.main_control.cut())

    # ----------------------------------------------------------------------
    def test_copy(self):
        self.assertIsNone(self.main_control.copy())

    # ----------------------------------------------------------------------
    def test_paste(self):
        self.assertIsNone(self.main_control.paste())

    # ----------------------------------------------------------------------
    def test_get_clipboard(self):
        self.assertIsNotNone(self.main_control.get_clipboard())
        #self.assertEqual("expected", self.main_control.get_clipboard())

    # ----------------------------------------------------------------------
    def test_reset_clipboard(self):
        self.assertIsNone(self.main_control.reset_clipboard())

    # ----------------------------------------------------------------------
    def test_preferences(self):
        self.assertIsNone(self.main_control.preferences())

    # ----------------------------------------------------------------------
    def test_delete(self):
        self.assertIsNone(self.main_control.delete())

    # ----------------------------------------------------------------------
    def test_run(self):
        code = None
        self.assertIsNone(self.main_control.run(code))
        code = "Teste"
        self.assertIsNone(self.main_control.run(code))

    # ----------------------------------------------------------------------
    def test_save_source(self):
        code = None
        self.assertIsNone(self.main_control.save_source(code))
        code = "Teste"
        self.assertIsNone(self.main_control.save_source(code))

    # ----------------------------------------------------------------------
    def test_view_source(self):
        self.assertIsNone(self.main_control.view_source())

    # ----------------------------------------------------------------------
    def test_about(self):
        self.assertIsNone(self.main_control.about())

    # ----------------------------------------------------------------------
    def test_search(self):
        query = None
        self.assertIsNone(self.main_control.search(query))
        query = "Teste"
        self.assertIsNone(self.main_control.search(query))

    # ----------------------------------------------------------------------
    def test_set_block(self):
        # from mosaicode.GUI.block import Block
        # from mosaicode.GUI.diagram import Diagram as Diagram
        # from mosaicode.model.plugin import Plugin as Plugin
        #
        # block = Block(Diagram, Plugin)
        # self.assertIsNone(self.main_control.set_block(block))
        self.assertIsNone(self.main_control.set_block("TESTE"))

        #block2 = None
        #self.assertIsNone(self.main_control.set_block(block2))

    # ----------------------------------------------------------------------
    def test_append_status_log(self):
        self.assertIsNone(self.main_control.append_status_log("TEXT"))
        #self.assertIsNone(self.main_control.append_status_log(None))

    # ----------------------------------------------------------------------
    def test_add_block(self):
        #from mosaicode.GUI.block import Block
        #from mosaicode.GUI.diagram import Diagram as Diagram
        #from mosaicode.model.plugin import Plugin as Plugin

        #block = Block(Diagram, Plugin)
        self.assertFalse(self.main_control.add_block(None))
        #self.assertFalse(self.main_control.add_block(block))
        self.assertFalse(self.main_control.add_block("TESTE"))

    # ----------------------------------------------------------------------
    def test_get_selected_block(self):
        #self.assertIsNotNone(self.main_control.get_selected_block())
        self.assertIsNone(self.main_control.get_selected_block())

    # ----------------------------------------------------------------------
    def test_zoom_in(self):
        self.assertIsNone(self.main_control.zoom_in())

    # ----------------------------------------------------------------------
    def test_zoom_out(self):
        self.assertIsNone(self.main_control.zoom_out())

    # ----------------------------------------------------------------------
    def test_zoom_normal(self):
        self.assertIsNone(self.main_control.zoom_normal())

    # ----------------------------------------------------------------------
    def test_show_block_property(self):
        block = "None"
        self.assertIsNone(self.main_control.show_block_property(block))

    # ----------------------------------------------------------------------
    def test_clear_console(self):
        self.assertIsNone(self.main_control.clear_console())

    # ----------------------------------------------------------------------
    def test_undo(self):
        self.assertIsNone(self.main_control.undo())

    # ----------------------------------------------------------------------
    def test_redo(self):
        self.assertIsNone(self.main_control.redo())

    # ----------------------------------------------------------------------
    def test_reload(self):
        self.assertIsNone(self.main_control.reload())


    # ---- METODOS DIFERENTES ------
    # ----------------------------------------------------------------------
    def test_align_top(self):
        self.assertFalse(self.main_control.align_top())

    # ----------------------------------------------------------------------
    def test_align_bottom(self):
        self.assertFalse(self.main_control.align_bottom())

    # ----------------------------------------------------------------------
    def test_align_left(self):
        self.assertFalse(self.main_control.align_left())

    # ----------------------------------------------------------------------
    def test_align_right(self):
        self.assertFalse(self.main_control.align_right())

    # ----------------------------------------------------------------------
    def test_redraw(self):
        show_grid = None
        self.assertIsNone(self.main_control.redraw(show_grid))

    # ----------------------------------------------------------------------
    def test_show_grid(self):
        event = "None"
        self.assertIsNone(self.main_control.show_grid(event))


    # ----------------------------------------------------------------------
    def test_code_template_manager(self):
        self.assertIsNone(self.main_control.code_template_manager())

    # ----------------------------------------------------------------------
    def test_plugin_manager(self):
        self.assertIsNone(self.main_control.plugin_manager())

    # ----------------------------------------------------------------------
    def test_port_manager(self):
        self.assertIsNone(self.main_control.port_manager())

    # ----------------------------------------------------------------------
    def test_add_code_template(self):
        #code_template = None
        #self.assertIsNone(self.main_control.add_code_template(code_template))
        from mosaicode.model.codetemplate import CodeTemplate

        code_template = CodeTemplate()

        code_template.type = "c"
        code_template.name = "TESTE"
        code_template.source = "xml"
        self.assertIsNone(self.main_control.add_code_template(code_template))


    # ----------------------------------------------------------------------
    def test_delete_code_template(self):
        #code_template_name = None
        #self.assertIsNone(self.main_control.delete_code_template(code_template_name))
        #from mosaicode.model.codetemplate import CodeTemplate

        code_template_name = "TESTE"
        self.assertIsNone(self.main_control.delete_code_template(code_template_name))

    # ----------------------------------------------------------------------
    def test_add_port(self):

        from mosaicode.model.port import Port

        port = Port()

        port.type = "c"
        port.language = "c"
        port.source = "xml"
        port.code = "xxxx"

        self.assertIsNone(self.main_control.add_port(port))

    # ----------------------------------------------------------------------
    def test_delete_port(self):

        from mosaicode.model.port import Port

        port = Port()

        port.type = "c"
        port.language = "c"
        port.source = "xml"
        port.code = "xxxx"

        self.assertIsNone(self.main_control.delete_port(port))

    # ----------------------------------------------------------------------
    def test_add_plugin(self):
        self.assertIsNone(self.main_control.add_plugin(None))

    # ----------------------------------------------------------------------
    def test_delete_plugin(self):
        self.assertIsNone(self.main_control.delete_plugin(None))

    # ----------------------------------------------------------------------
    def test_update_all(self):
        self.assertIsNone(self.main_control.update_all())

    # ----------------------------------------------------------------------
    def test_print_ports(self):
        self.assertIsNone(self.main_control.print_ports())

    # ----------------------------------------------------------------------
    def test_print_plugins(self):
        self.assertIsNone(self.main_control.print_plugins())

    # ----------------------------------------------------------------------
    def test_print_templates(self):
        self.assertIsNone(self.main_control.print_templates())

    # ----------------------------------------------------------------------
    def test_export_extensions(self):
        self.assertIsNone(self.main_control.export_extensions(None))

    # ----------------------------------------------------------------------
    def test_export_python(self):
        self.assertIsNone(self.main_control.export_python())

    # ----------------------------------------------------------------------
    def test_export_python_dialog(self):
        self.assertIsNone(self.main_control.export_python_dialog())

    # ----------------------------------------------------------------------
    def test_export_xml(self):
        self.assertIsNone(self.main_control.export_xml())

    # ----------------------------------------------------------------------
    def test_export_xml_dialog(self):
        self.assertIsNone(self.main_control.export_xml_dialog())

    # ----------------------------------------------------------------------
    def test_add_recent_file(self):
        #prefs = ?
        from mosaicode.model.preferences import Preferences

        prefs = Preferences()

        file_name = "Untitled.mscd"
        self.assertIsNone(self.main_control.add_recent_file(prefs, file_name))
