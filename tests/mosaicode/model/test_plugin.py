from tests.test_base import TestBase
from mosaicode.model.plugin import Plugin

class TestPlugin(TestBase):

    def test_init(self):
        model = Plugin()
