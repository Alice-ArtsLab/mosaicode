import gi
from gi.repository import GObject
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from tests.test_base import TestBase
from mosaicode.GUI.workarea import WorkArea

class TestWorkArea(TestBase):

    def setUp(self):
        self.workarea = WorkArea(self.create_main_window())

    def test_add_diagram(self):
        self.workarea.add_diagram(self.create_diagram())
        self.workarea.add_diagram(self.create_diagram())
        self.workarea.add_diagram(self.create_diagram())

    def close_window(self):
        self.workarea.dialog.response(Gtk.ResponseType.CANCEL)
        self.workarea.dialog.destroy()

    def test_close_tab(self):
        GObject.timeout_add(100, self.close_window)
        self.workarea.close_tab()
        self.workarea.close_tab(0)
        diagram = self.create_diagram()
        diagram.set_modified(True)
        self.workarea.add_diagram(diagram)
        self.workarea.close_tab(0)

    def test_rename_diagram(self):
        diagram = self.create_diagram()
        self.workarea.add_diagram(diagram)
        diagram.set_modified(True)
        self.workarea.rename_diagram(diagram)

    def test_get_diagrams(self):
        self.workarea.get_diagrams()

    def test_resize(self):
        self.workarea.add_diagram(self.create_diagram())
        self.workarea.resize(None)

    def test_close_tabs(self):
        GObject.timeout_add(100, self.close_window)
        diagram = self.create_diagram()
        self.workarea.add_diagram(diagram)
        diagram.set_modified(True)
        self.workarea.close_tabs()

    def test_get_current_diagram(self):
        self.workarea.add_diagram(self.create_diagram())
        self.workarea.get_current_diagram()
        self.workarea.close_tabs()
        self.workarea.get_current_diagram()

    def test_events(self):
        gdkevent = Gdk.Event()
        gdkevent.key.type = Gdk.EventType.BUTTON_PRESS
        self.workarea.add_diagram(self.create_diagram())
        tab = self.workarea.get_nth_page(self.workarea.get_current_page())
        hbox = self.workarea.get_tab_label(tab)
        label = hbox.get_children()[0]
        button = hbox.get_children()[1]
        button.emit("clicked")

