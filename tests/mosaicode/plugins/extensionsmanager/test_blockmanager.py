import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import threading
from time import sleep
from tests.mosaicode.test_base import TestBase
from mosaicode.plugins.extensionsmanager.blockmanager \
    import BlockManager

class TestBlockManager(TestBase):

    def setUp(self):
        self.widget = BlockManager(self.create_main_window())

    def test_update(self):
        self.widget.update()
        self.close_window()

    def test_add_new_block(self):
        self.widget.add_new_block(self.create_block())
        self.close_window()

    def close_window(self):
        self.widget.close()
        self.widget.destroy()

    def test_events(self):
        # Add Button
        self.setUp()
        self.event_button1()
        self.close_window()

        # Edit Button with None
        self.setUp()
        self.event_button2()
        self.close_window()

        # Edit button with Selected
        self.setUp()
        self.widget.block_notebook.set_current_page(0)
        self.event_button2()
        self.close_window()

        # Delete button with None
        self.setUp()
        self.widget.run()
        self.event_button3()
        self.close_window()

        # Delete button with Selected
        self.setUp()
        self.widget.block_notebook.set_current_page(0)
        self.event_button3()
        self.close_window()

    def event_button1(self):
        box = self.widget.get_children()[0]
        vbox = box.get_children()[0]
        button_bar = vbox.get_children()[1]
        button1 = button_bar.get_children()[0].emit("clicked")

    def event_button2(self):
        box = self.widget.get_children()[0]
        vbox = box.get_children()[0]
        button_bar = vbox.get_children()[1]
        button2 = button_bar.get_children()[1].emit("clicked")

    def event_button3(self):
        sleep(1)
        box = self.widget.get_children()[0]
        vbox = box.get_children()[0]
        button_bar = vbox.get_children()[1]
        button3 = button_bar.get_children()[2].emit("clicked")
        self.close_window()

