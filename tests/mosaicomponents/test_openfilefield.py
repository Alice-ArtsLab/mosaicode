import unittest
from mosaicomponents.openfilefield import OpenFileField

class TestOpenFileField(unittest.TestCase):

    def setUp(self):
        OpenFileField(None, None)
        self.field = OpenFileField({"label": "test", "value": "False"}, None)
        self.field = OpenFileField({"label": "test", "value": "True"}, None)
        self.field = OpenFileField({}, self.test_value)
        self.field.set_parent_window(None)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

