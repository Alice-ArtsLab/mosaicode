from tests.test_base import TestBase
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port

class TestCodeTemplate(TestBase):

    def test_init(self):
        code1 = CodeTemplate()
        code2 = CodeTemplate()
        self.assertEquals(code1.equals(code2), True)

        code1.language = "Test"
        self.assertEquals(code1.equals(code2), False)

        code1 = CodeTemplate()
        code1.__dict__.pop(code1.__dict__.keys()[0], None)
        self.assertEquals(code2.equals(code1), False)
