import unittest
from mosaicomponents.colorfield import ColorField

class TestColorField(unittest.TestCase):

    def setUp(self):
        ColorField(None, None)
        self.field = ColorField({"label": "test", "value": "#fff"}, None)
        self.field = ColorField({"label": "test", "value": "#fff000"}, None)
        self.field = ColorField({}, self.test_value)
        self.field.set_parent_window(None);

    def test_value(self):

        self.field = ColorField({"value": "#fff","format": "FFF"}, None)
        value1 = "#fff"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": "FFFFFF"}, None)
        value1 = "#f0f0f0"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": "FFFFFFFFF"}, None)
        value1 = "#f0f0f0"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual("#f00f00f00", value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": "FFFFFFFF"}, None)
        value1 = 0
        self.field.set_value(int(value1))
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

