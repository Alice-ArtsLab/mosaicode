from unittest import TestCase
from harpia.GUI.workarea import WorkArea

class TestWorkArea(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.work_area = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_add_diagram(self):
        self.work_area.add_diagram()

    # ----------------------------------------------------------------------x
    def test_close_tab(self):
        self.work_area.close_tab()

    # ----------------------------------------------------------------------x
    def test_get_current_diagram(self):
        self.work_area.get_current_diagram()

    # ----------------------------------------------------------------------x
    def test_rename_diagram(self):
        self.work_area.rename_diagram()

    # ----------------------------------------------------------------------x
    def test_resize(self):
        self.work_area.resize()

    # ----------------------------------------------------------------------x
    def test_close_tabs(self):
        self.work_area.close_tabs()
