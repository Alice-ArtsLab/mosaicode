import unittest
from mosaicomponents.field import Field

class TestField(unittest.TestCase):

    def setUp(self):
        Field(None, None)
        self.field = Field({"label": "test", "value": "False"}, None)
        self.field = Field({"label": "test", "value": "True"}, None)
        self.field = Field({}, self.test_value)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

