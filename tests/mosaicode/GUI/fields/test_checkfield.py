import unittest
from mosaicode.GUI.fields.checkfield import CheckField

class TestCheckField(unittest.TestCase):

    def setUp(self):
        CheckField(None, None)
        self.field = CheckField({"label": "test", "value": "False"}, None)
        self.field = CheckField({"label": "test", "value": "True"}, None)
        self.field = CheckField({}, self.test_value)

    def test_value(self):
        value1 = False
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = True
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

