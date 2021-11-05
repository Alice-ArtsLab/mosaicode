import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from tests.mosaicode.test_base import TestBase
from mosaicode.GUI.diagrammenu import DiagramMenu

class TestDiagramMenu(TestBase):

    def setUp(self):
        self.diagrammenu = DiagramMenu()

    def test_show(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        self.diagrammenu.show(self.create_diagram(), event)

        self.diagrammenu.uncollapse_menu_item.emit("activate")
        self.refresh_gui()
        self.diagrammenu.collapse_menu_item.emit("activate")
        self.refresh_gui()
        self.diagrammenu.clear_menu_item.emit("activate")
        self.refresh_gui()
        self.diagrammenu.insert_menu_item.emit("activate")
        self.refresh_gui()
        self.diagrammenu.delete_menu_item.emit("activate")
        self.refresh_gui()
        self.diagrammenu.destroy()
