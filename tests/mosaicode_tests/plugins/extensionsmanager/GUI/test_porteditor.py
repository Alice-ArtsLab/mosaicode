import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.system import System
from mosaicode.plugins.extensionsmanager.GUI.portmanager import PortManager
from mosaicode.plugins.extensionsmanager.GUI.porteditor import PortEditor

class TestPortEditor(TestBase):

    def setUp(self):
        self.port_manager = PortManager(self.create_main_window())
        self.widget = PortEditor(self.port_manager, None)

    def close_window(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        self.widget.emit("button-press-event", event)
        self.widget.response(Gtk.ResponseType.OK)

    def test_base(self):
        GLib.timeout_add(100, self.close_window)
        port = self.create_port()
        self.widget = PortEditor(self.port_manager, port.type)
        self.widget.response(Gtk.ResponseType.OK)

        GLib.timeout_add(100, self.close_window)
        self.port_manager.add_port(port)
        self.widget = PortEditor(self.port_manager, port.type)

