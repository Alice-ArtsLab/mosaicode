import unittest
from mosaicomponents.intfield import IntField

class TestIntField(unittest.TestCase):

    def setUp(self):
        IntField(None, None)
        self.field = IntField({"label": "test", "value": 1}, None)
        self.field = IntField({"label": "test", "value": 0}, None)
        self.field = IntField({}, self.test_value)

    def test_value(self):
        value1 = 0
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = 100
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

