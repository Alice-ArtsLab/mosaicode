import unittest
from mosaicomponents.combofield import ComboField

class TestComboField(unittest.TestCase):

    def setUp(self):
        ComboField(None, None)
        self.field = ComboField({"label": "test", "value": False}, None)
        self.field = ComboField({"label": "test", "value": True}, None)
        self.field = ComboField({}, self.test_value)

    def test_value(self):
        value1 = False
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = True
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

