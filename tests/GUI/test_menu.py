from tests.test_base import TestBase
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

    def test_update_examples(self):
        System.list_of_examples.append("teste")
        self.menu.update_examples(System.list_of_examples)
        self.menu.update_examples(System.list_of_examples)

    def test_update_blocks(self):
        self.menu.update_blocks(System.get_blocks())
        self.menu.update_blocks(System.get_blocks())
