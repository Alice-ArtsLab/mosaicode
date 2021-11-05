import unittest
from mosaicode.GUI.fields.commentfield import CommentField

class TestCommentField(unittest.TestCase):

    def setUp(self):
        CommentField(None, None)
        self.field = CommentField({"label": "test", "value": "False"}, None)
        self.field = CommentField({"label": "test", "value": "True"}, None)
        self.field = CommentField({}, self.test_value)

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

