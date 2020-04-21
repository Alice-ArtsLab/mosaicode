import unittest
from mosaicomponents.savefilefield import SaveFileField

class TestSaveFileField(unittest.TestCase):

    def setUp(self):
        SaveFileField(None, None)
        self.field = SaveFileField({"label": "test", "value": "False"}, None)
        self.field = SaveFileField({"label": "test", "value": "True"}, None)
        self.field = SaveFileField({}, self.test_value)
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

