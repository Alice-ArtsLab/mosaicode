import unittest
from mosaicode.GUI.fields.combofield import ComboField

class TestComboField(unittest.TestCase):

    def setUp(self):
        ComboField(None, None)
        data = {"label": "Test", "value": "a", "name": "", "values": ["a"]}
        self.field = ComboField(data, None)
        self.field = ComboField({"label": "test", "value": True}, None)
        self.field = ComboField({}, self.test_value)

    def test_value(self):
        data = {"label": "Test", "value": "a", "name": "", "values": ["a"]}
        self.field = ComboField(data, None)
        value1 = "a"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
