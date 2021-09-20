import unittest
from mosaicode.GUI.fields.codefield import CodeField

class TestCodeField(unittest.TestCase):

    def setUp(self):
        CodeField(None, None)
        self.field = CodeField({"label": "test", "value": "False"}, None)
        self.field = CodeField({"label": "test", "value": "True"}, None)
        self.field = CodeField({}, self.test_value)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        self.field.insert_at_cursor("Test")

