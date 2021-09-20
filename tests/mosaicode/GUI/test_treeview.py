import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode.test_base import TestBase
from mosaicode.GUI.treeview import TreeView

class TestTreeView(TestBase):

    def setUp(self):
        self.treeview = TreeView("Title", self.action, None)

    def action(self):
        pass

    def test_populate(self):
        items = ["A", "B", "C"]
        self.treeview.populate(items)

    def test_get_selection(self):
        self.treeview.get_selection()
