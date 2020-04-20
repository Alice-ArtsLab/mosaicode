from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmenuitem \
    import BlockMenuItem


class TestBlockMenuItem(TestBase):

    def setUp(self):
        self.widget = BlockMenuItem(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = BlockMenuItem(
                        None,
                        self.create_block())

