from unittest import TestCase
from harpia.GUI.searchbar import SearchBar

class TestSearchBar(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.search_bar = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_search_changed(self):
        self.search_bar.search_changed()

    