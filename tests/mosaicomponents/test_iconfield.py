import unittest
from mosaicomponents.iconfield import IconField

class TestIconField(unittest.TestCase):

    def setUp(self):
        IconField(None, None)
        self.field = IconField({"label": "test", "value": "False"}, None)
        self.field = IconField({"label": "test", "value": "True"}, None)
        self.field = IconField({}, self.test_value)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

