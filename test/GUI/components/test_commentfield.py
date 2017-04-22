from unittest import TestCase
from harpia.GUI.components.commentfield import CommentField

class TestCommentField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.comment_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.comment_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.comment_field.get_value()
