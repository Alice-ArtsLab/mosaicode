from tests.test_base import TestBase
from mosaicode.GUI.status import Status


class TestStatus(TestBase):

    def setUp(self):
        self.status = Status(self.create_main_window())

    def test_clear(self):
        self.assertIsNone(self.status.clear())

    def test_append_text(self):
        self.assertIsNone(self.status.append_text("test_append_text"))

    def test_log(self):
        self.assertIsNone(self.status.log("test_append_text"))

