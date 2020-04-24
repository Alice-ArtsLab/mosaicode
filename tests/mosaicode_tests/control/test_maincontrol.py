from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.maincontrol import MainControl


class TestMainControl(TestBase):

    def setUp(self):
        self.main_control = MainControl(self.create_main_window())

    def test_add_block(self):
        self.main_control.add_block(self.create_block())

    def test_add_code_template(self):
        self.main_control.add_code_template(self.create_code_template())

    def test_add_comment(self):
        self.main_control.add_comment()

    def test_add_new_block(self):
        self.main_control.add_new_block(self.create_block())

    def test_add_port(self):
        self.main_control.add_port(self.create_port())

    def test_align_bottom(self):
        self.main_control.align_bottom()

    def test_align_left(self):
        self.main_control.align_left()

    def test_align_right(self):
        self.main_control.align_right()

    def test_align_top(self):
        self.main_control.align_top()

    def test_clear_console(self):
        self.main_control.clear_console()

    def test_close(self):
        self.main_control.close()

    def test_collapse_all(self):
        self.main_control.collapse_all()

    def test_copy(self):
        self.main_control.copy()

    def test_cut(self):
        self.main_control.cut()

    def test_delete(self):
        self.main_control.delete()

    def test_delete_block(self):
        self.main_control.delete_block(self.create_block())

    def test_delete_code_template(self):
        self.main_control.delete_code_template(self.create_code_template())

    def test_delete_port(self):
        self.main_control.delete_port("port_key")

    def test_exit(self):
        self.main_control.exit()

    def test_export_diagram(self):
        self.main_control.export_diagram()

    def test_get_clipboard(self):
        self.main_control.get_clipboard()

    def test_get_selected_block(self):
        self.main_control.get_selected_block()

    def test_init(self):
        self.main_control.init()

    def test_new(self):
        self.main_control.new()

    def test_open(self):
        self.main_control.open("Test")

    def test_paste(self):
        self.main_control.paste()

    def test_preferences(self):
        self.main_control.preferences()

    def test_publish(self):
        self.main_control.publish()

    def test_redo(self):
        self.main_control.redo()

    def test_redraw(self):
        self.main_control.redraw(True)
        self.main_control.redraw(False)

    def test_reset_clipboard(self):
        self.main_control.reset_clipboard()

    def test_run(self):
        self.main_control.run()

    def test_save(self):
        self.main_control.save()
        self.main_control.save(save_as=True)

    def test_save_as(self):
        self.main_control.save_as()

    def test_save_as_example(self):
        self.main_control.save_as_example()

    def test_save_source(self):
        self.main_control.save_source()
        self.main_control.save_source(codes="Test")
        self.main_control.save_source(generator="Test")

    def test_search(self):
        self.main_control.search("Test")

    def test_select_all(self):
        self.main_control.select_all()

    def test_select_open(self):
        self.main_control.select_open()

    def test_set_block(self):
        self.main_control.set_block(self.create_block())

    def test_set_recent_files(self):
        self.main_control.set_recent_files("Test")

    def test_show_grid(self):
        self.main_control.show_grid(None)

    def test_stop(self):
        self.main_control.stop(None, None)

    def test_uncollapse_all(self):
        self.main_control.uncollapse_all()

    def test_undo(self):
        self.main_control.undo()

    def test_update_all(self):
        self.main_control.update_all()

    def test_update_blocks(self):
        self.main_control.update_blocks()

    def test_view_source(self):
        self.main_control.view_source()

    def test_zoom_in(self):
        self.main_control.zoom_in()

    def test_zoom_normal(self):
        self.main_control.zoom_normal()

    def test_zoom_out(self):
        self.main_control.zoom_out()

