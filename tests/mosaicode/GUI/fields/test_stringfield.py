import unittest
from mosaicode.GUI.fields.stringfield import StringField

class TestStringField(unittest.TestCase):

    def setUp(self):
        StringField(None, None)
        self.field = StringField({"label": "test", "value": "False"}, None)
        self.field = StringField({"label": "test", "value": "True"}, None)
        self.field = StringField({}, self.test_value)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

