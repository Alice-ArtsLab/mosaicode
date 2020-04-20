import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.selectcodetemplate import SelectCodeTemplate
from mosaicode.system import System as System

class TestSelectCodeTemplate(TestBase):

    def close_window(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        self.selectcodetemplate.emit("button-press-event", event)
        self.selectcodetemplate.response(Gtk.ResponseType.OK)
        self.selectcodetemplate.response(Gtk.ResponseType.CANCEL)
        self.selectcodetemplate.close()
        self.selectcodetemplate.destroy()

    def setUp(self):
        GLib.timeout_add(100, self.close_window)
        self.selectcodetemplate = SelectCodeTemplate(
                self.create_main_window(), System.get_code_templates())
        self.selectcodetemplate.destroy()

    def test_get_value(self):
        self.selectcodetemplate.get_value()

