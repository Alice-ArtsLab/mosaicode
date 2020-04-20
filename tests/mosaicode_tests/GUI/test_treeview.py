import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.treeview import TreeView

class TestTreeView(TestBase):

    def setUp(self):
        self.treeview = TreeView("Title", None, None)
