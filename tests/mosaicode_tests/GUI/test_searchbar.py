from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.searchbar import SearchBar


class TestStatus(TestBase):

    def setUp(self):
        self.searchbar = SearchBar(self.create_main_window())

    def test_search_changed(self):
        self.searchbar.search_changed(None)

