from tests.test_base import TestBase
from mosaicode.model.connectionmodel import ConnectionModel

class TestConnectionModel(TestBase):

    def test_init(self):
        ConnectionModel(None, None, None)
