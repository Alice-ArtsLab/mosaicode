import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.comment import Comment

class TestComment(TestBase):

    def setUp(self):
        self.comment = self.create_comment()

    def test_move(self):
        self.comment.move(10,10)
