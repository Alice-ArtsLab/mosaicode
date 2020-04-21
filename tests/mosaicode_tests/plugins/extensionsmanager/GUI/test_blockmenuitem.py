from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmenuitem \
    import BlockMenuItem


class TestBlockMenuItem(TestBase):

    def setUp(self):
        self.widget = BlockMenuItem(self.create_main_window())

    def test_base(self):
        self.widget.emit("activate")

