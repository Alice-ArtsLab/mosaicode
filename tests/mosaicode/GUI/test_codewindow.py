from tests.test_base import TestBase
from mosaicode.GUI.codewindow import CodeWindow


class TestCodeWindow(TestBase):

    def setUp(self):
        pass

    def test_init(self):
        self.code_window = CodeWindow(self.create_main_window(),"int main()")
        self.code_window.close()
        self.code_window.destroy()
