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

    def setUp(self):
        GLib.timeout_add(100, self.close_window)
        System()
        code_template = self.create_code_template()
        template_list = {code_template}
        main_window = self.create_main_window()
        self.selectcodetemplate = SelectCodeTemplate(main_window, template_list)
        self.selectcodetemplate.destroy()

    def close_window(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        self.selectcodetemplate.emit("button-press-event", event)
        self.refresh_gui()
        self.selectcodetemplate.response(Gtk.ResponseType.OK)
        self.refresh_gui()
        self.selectcodetemplate.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        self.selectcodetemplate.close()
        self.selectcodetemplate.destroy()

    def test_get_value(self):
        self.selectcodetemplate.get_value()

