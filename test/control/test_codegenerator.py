from unittest import TestCase
from harpia.control.codegenerator import CodeGenerator
from harpia.GUI.diagram import Diagram
from harpia.GUI.block import Block
from harpia.GUI.mainwindow import MainWindow



class TestCodeGenerator(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        diagram = Diagram(win)
        block = Block()
        self.code_generator = CodeGenerator(diagram)

    # ----------------------------------------------------------------------
    def test_replace_wildcards(self):
        self.code_generator.replace_wildcards("Teste")

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
    def test_generate_code(self):
        self.code_generator.generate_code()

    # ----------------------------------------------------------------------
    def test_save_code(self):
        self.code_generator.save_code()

    # ----------------------------------------------------------------------
    def test_compile(self):
        self.code_generator.compile()

    # ----------------------------------------------------------------------
    def test_execute(self):
        self.code_generator.execute()
