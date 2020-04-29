import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.blockmenu import BlockMenu

class TestBlockMenu(TestBase):

    def setUp(self):
        self.blockmenu = BlockMenu()

    def test_show(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        self.blockmenu.show(self.create_block(), event)

        self.blockmenu.collapse_menu_item.emit("activate")
        self.refresh_gui()
        self.blockmenu.delete_menu_item.emit("activate")
        self.refresh_gui()
        self.blockmenu.destroy()
