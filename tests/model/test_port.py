from tests.test_base import TestBase
from mosaicode.model.port import Port

class TestPort(TestBase):

    def test_init(self):
        model = Port()
        self.assertEqual(model.is_input(), False)
        model.conn_type = Port.INPUT
        self.assertEqual(model.is_input(), True)
        model.conn_type = Port.OUTPUT
        self.assertEqual(model.is_input(), False)

