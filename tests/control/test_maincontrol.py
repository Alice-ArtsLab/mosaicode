from unittest import TestCase
from mosaicode.control.maincontrol import MainControl
from mosaicode.GUI.mainwindow import MainWindow


class TestMainControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------
    def test_new(self):
        self.main_control.new()

    # ----------------------------------------------------------------------
    def test_select_open(self):
        self.main_control.select_open()

    # ----------------------------------------------------------------------
    def test_open(self):
        self.main_control.open("app_data/examples/Add Border.mscd")

    # ----------------------------------------------------------------------
    def test_close(self):
        self.main_control.close()

    # ----------------------------------------------------------------------
    def test_save(self):
        self.main_control.save()

    # ----------------------------------------------------------------------
    def test_save_as(self):
        self.main_control.save_as()

    # ----------------------------------------------------------------------
    def test_rename_tab(self):
        self.main_control.rename_tab()

    # ----------------------------------------------------------------------
    def test_export_diagram(self):
        self.main_control.export_diagram()

    # ----------------------------------------------------------------------
    def test_exit(self):
        self.main_control.exit()

    # ----------------------------------------------------------------------
    def test_select_all(self):
        self.main_control.select_all()

    # ----------------------------------------------------------------------
    def test_cut(self):
        self.main_control.cut()

    # ----------------------------------------------------------------------
    def test_copy(self):
        self.main_control.copy()

    # ----------------------------------------------------------------------
    def test_paste(self):
        self.main_control.paste()

    # ----------------------------------------------------------------------
    def test_get_clipboard(self):
        self.main_control.get_clipboard()

    # ----------------------------------------------------------------------
    def test_reset_clipboard(self):
        self.main_control.reset_clipboard()

    # ----------------------------------------------------------------------
    def test_preferences(self):
        self.main_control.get_preferences()

    # ----------------------------------------------------------------------
    def test_delete(self):
        self.main_control.delete()

    # ----------------------------------------------------------------------
    def test_run(self):
        self.main_control.run()

    # ----------------------------------------------------------------------
    def test_save_source(self):
        self.main_control.save_source()

    # ----------------------------------------------------------------------
    def test_view_source(self):
        self.main_control.view_source()

    # ----------------------------------------------------------------------
    def test_about(self):
        self.main_control.about()

    # ----------------------------------------------------------------------
    def test_search(self):
        self.main_control.search()

    # ----------------------------------------------------------------------
    def test_set_block(self):
        self.main_control.set_block()

    # ----------------------------------------------------------------------
    def test_append_status_log(self):
        self.main_control.append_status_log("TEXT")

    # ----------------------------------------------------------------------
    def test_add_block(self):
        self.main_control.add_block("TESTE")

    # ----------------------------------------------------------------------
    def test_get_selected_block(self):
        self.main_control.get_selected_block()

    # ----------------------------------------------------------------------
    def test_zoom_in(self):
        self.main_control.zoom_in()

    # ----------------------------------------------------------------------
    def test_zoom_out(self):
        self.main_control.zoom_out()

    # ----------------------------------------------------------------------
    def test_zoom_normal(self):
        self.main_control.zoom_normal()

    # ----------------------------------------------------------------------
    def test_show_block_property(self):
        self.main_control.show_block_property()

    # ----------------------------------------------------------------------
    def test_clear_console(self):
        self.main_control.clear_console()

    # ----------------------------------------------------------------------
    def test_undo(self):
        self.main_control.undo()

    # ----------------------------------------------------------------------
    def test_redo(self):
        self.main_control.redo()

    # ----------------------------------------------------------------------
    def test_reload(self):
        self.main_control.reload()
