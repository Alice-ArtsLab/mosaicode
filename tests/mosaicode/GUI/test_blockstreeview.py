from tests.mosaicode.test_base import TestBase
from mosaicode.system import System as System
from mosaicode.GUI.blockstreeview import BlocksTreeView


class TestBlocksTreeView(TestBase):

    def setUp(self):
        block1 = self.create_block()
        block1.group = "Test2"
        self.widget = BlocksTreeView(
                    self.create_main_window(),
                    "Test",
                    {"Test1" : block1,
                     "Test2" : self.create_block()})

    def test_get_selected_block(self):
        self.widget.get_selected_block()

    def test_row_activated(self):
        treeselection = self.widget.blocks_tree_view.get_selection()
        treeselection.select_iter(self.widget.tree_store.get_iter_first())
        model, iterac = treeselection.get_selected()
        path = model.get_path(iterac)
        column = self.widget.blocks_tree_view.get_column(0)
        self.blockstreeview.blocks_tree_view.row_activate(path, column)

    def test_events(self):
        self.widget.blocks_tree_view.emit("cursor-changed")
        self.widget.blocks_tree_view.emit("drag-data-get")
        self.refresh_gui()
