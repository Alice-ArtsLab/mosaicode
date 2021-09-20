from tests.mosaicode.test_base import TestBase
from mosaicode.GUI.codewindow import CodeWindow


class TestCodeWindow(TestBase):

    def setUp(self):
        pass

    def test_init(self):
        codes = {'color': 'blue', 'fruit': 'apple', 'pet': 'dog'}
        self.code_window = CodeWindow(self.create_main_window(), codes)
        self.code_window.save_button.emit("clicked")
        self.code_window.run_button.emit("clicked")
        self.code_window.close()
        self.code_window.destroy()
