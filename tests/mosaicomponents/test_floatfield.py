import unittest
from mosaicomponents.floatfield import FloatField

class TestFloatField(unittest.TestCase):

    def setUp(self):
        FloatField(None, None)
        self.field = FloatField({"label": "test", "value": 0.5}, None)
        self.field = FloatField({"label": "test", "value": -1}, None)
        self.field = FloatField({}, self.test_value)

    def test_value(self):
        value1 = -0.5
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = 12
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

