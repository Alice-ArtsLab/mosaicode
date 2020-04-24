from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.codegenerator import CodeGenerator


class TestCodeGenerator(TestBase):

    def setUp(self):
        self.code_generator = CodeGenerator(self.create_diagram())

    def test_generate_code(self):
        self.code_generator.generate_code()
