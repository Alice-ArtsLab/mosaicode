import unittest
from mosaicomponents.labelfield import LabelField

class TestLabelField(unittest.TestCase):

    def setUp(self):
        LabelField(None, None)
        self.field = LabelField({"label": "test"}, None)
        self.field = LabelField({"label": "test"}, None)
        self.field = LabelField({}, self.test_value)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

