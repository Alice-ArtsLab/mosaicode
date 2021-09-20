import unittest
from mosaicode.GUI.fields.field import Field

class TestField(unittest.TestCase):

    def setUp(self):
        Field(None, None)
        self.field = Field({"label": "test", "value": "False"}, None)
        self.field = Field({"label": "test", "value": "True"}, None)
        self.field = Field({}, self.test_value)

    def test_value(self):
        self.field.set_value(1)
        self.field.get_value()

