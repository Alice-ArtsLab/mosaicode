import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.menu import Menu
from mosaicode.system import System

class TestMenu(TestBase):

    def setUp(self):
        self.menu = Menu(self.create_main_window())

    def test_new(self):
        self.menu = Menu(self.create_main_window())

    def test_add_help(self):
        self.menu.add_help()

    def test_event(self):
        menuitem = self.menu.help_menu.get_children()[0]
        menuitem.emit("activate")
        self.refresh_gui()

    def test_update_examples(self):
        System.get_list_of_examples().append("language/framework/test")
        System.get_list_of_examples().append("language/framework/test1")
        self.menu.update_examples(System.get_list_of_examples())
        System.get_list_of_examples().append("test")
        self.menu.update_examples(System.get_list_of_examples())
        # language
        self.menu.example_menu.get_children()[0].activate()
        # extension
        self.menu.example_menu.get_children()[0].get_children()[0].activate()

    def test_update_recent_files(self):
        self.menu.update_recent_files(["file1", "file2"])
        self.menu.update_recent_files(["file1", "file2"])
        self.menu.update_recent_files(None)

    def test_update_blocks(self):
        self.menu.update_blocks(System.get_blocks())
        self.menu.update_blocks(System.get_blocks())

    def test_menu_item(self):
        self.menu.actions.keys()[0].emit("activate")
        self.refresh_gui()

    def test_recent_files(self):
        self.menu.update_recent_files(["file1", "file2"])
        self.menu.recent_files_menu.get_children()[0].emit("activate")
        self.refresh_gui()

    def test_event(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.KEY_PRESS
        event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
        event.keyval = Gdk.KEY_a
        self.menu.emit("key-press-event", event)
        self.refresh_gui()
        self.menu.emit("check-resize")
        self.refresh_gui()
        self.menu.emit("delete_event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_b
        self.menu.emit("key-press-event", event)
        self.refresh_gui()

