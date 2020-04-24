from tests.mosaicode_tests.test_base import TestBase
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port

class TestCodeTemplate(TestBase):

    # ----------------------------------------------------------------------
    def test_init(self):
        CodeTemplate()

    # ----------------------------------------------------------------------
    def test_equals(self):
        code1 = CodeTemplate()
        code2 = CodeTemplate()
        self.assertEquals(code1.equals(code2), True)

        code1.language = "Test"
        self.assertEquals(code1.equals(code2), False)

        code1 = CodeTemplate()
        code1.__dict__.pop(code1.__dict__.keys()[0], None)
        self.assertEquals(code2.equals(code1), False)

    # ----------------------------------------------------------------------
    def test_set_properties(self):
        code = CodeTemplate()
        code.properties  = [{"name": "test",
                             "label": "test",
                             "value": "test",
                             "type": "test"}]

        code.set_properties({"name": "test",
                             "label": "SET",
                             "value": "test",
                             "type": "test"})
#        assert code.properties[0]["label"] == "SET"

    # ----------------------------------------------------------------------
    def test_get_properties(self):
        code = CodeTemplate()
        properties = code.get_properties()
        assert isinstance(properties, list)

    # ----------------------------------------------------------------------
    def test_str(self):
        code = CodeTemplate()
        string = code.__str__()
        assert isinstance(string, str)
        assert string == str(code.__class__.__module__)
