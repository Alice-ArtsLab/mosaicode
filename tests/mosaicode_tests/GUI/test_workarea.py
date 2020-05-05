import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject
from gi.repository import GLib
from time import sleep
import threading
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.workarea import WorkArea

class TestWorkArea(TestBase):

    def setUp(self):
        self.workarea = WorkArea(self.create_main_window())

    def test_add_diagram(self):
        self.workarea.add_diagram(self.create_diagram())

    def close_window(self):
        self.workarea.destroy()

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

    def test_close_tab(self):
        diagram = self.create_diagram()
        self.workarea.add_diagram(diagram)
        self.workarea.close_tab(1000)

    def test_close_tabs(self):
        diagram = self.create_diagram()
        self.workarea.add_diagram(diagram)
        diagram.set_modified(True)
        t1 = threading.Thread(target=self.workarea.close_tabs, args=());
        t1.start()
        sleep(1)
        self.workarea.confirm.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

        t1 = threading.Thread(target=self.workarea.close_tab, args=());
        t1.start()
        sleep(1)
        self.workarea.confirm.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

        t1 = threading.Thread(target=self.workarea.close_tab, args=(-2));
        t1.start()
        sleep(1)
        self.workarea.confirm.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

        self.workarea.destroy()

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
        self.refresh_gui()

