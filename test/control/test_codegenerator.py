from unittest import TestCase
from harpia.control.codegenerator import CodeGenerator

class TestCodeGenerator(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------
    def test_replace_wildcards(self):
        self.code_generator.replace_wildcards()

    # ----------------------------------------------------------------------
    def test_get_dir_name(self):
        self.code_generator.get_dir_name()

    # ----------------------------------------------------------------------
    def test_get_filename(self):
        self.code_generator.get_filename()

    # ----------------------------------------------------------------------
    def test_change_directory(self):
        self.code_generator.change_directory()

    # ----------------------------------------------------------------------
    def test_sort_blocks(self):
        self.code_generator.sort_blocks()

    # ----------------------------------------------------------------------
    def test_get_max_weight(self):
        self.code_generator.get_max_weight()

    # ----------------------------------------------------------------------
    def test_generate_parts(self):
        self.code_generator.generate_parts()

    # ----------------------------------------------------------------------
    def test_generate_block_code(self):
        self.code_generator.generate_block_code()

    # ----------------------------------------------------------------------
    def test_save_code(self):
        self.code_generator.save_code()

    # ----------------------------------------------------------------------
    def test_compile(self):
        self.code_generator.compile()

    # ----------------------------------------------------------------------
    def test_execute(self):
        self.code_generator.execute()