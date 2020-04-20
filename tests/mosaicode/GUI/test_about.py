from tests.test_base import TestBase
from mosaicode.GUI.about import About


class TestAbout(TestBase):

    def setUp(self):
        self.about = About(self.create_main_window())

    def test_get_default_size(self):
        self.assertEqual(self.about.get_default_size(), (650, 480), 'incorrect size')

