import os
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.system import System
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence

class PreferencesPersistenceTest(TestBase):

    def test_load_save(self):
        System()
        prefs = System.get_preferences()
        PreferencesPersistence.save(prefs, "/tmp")
        PreferencesPersistence.save(prefs, "/etc")
        PreferencesPersistence.load("/tmp")
        PreferencesPersistence.load("/not")
        os.remove("/tmp/" + prefs.conf_file_path)

        code_template = self.create_code_template()
        code_template.name = "configuration"
        CodeTemplatePersistence.save_xml(code_template, "/tmp/")
        result = PreferencesPersistence.load("/tmp")
        file_name = "/tmp/" + code_template.name + ".xml"
        os.remove(file_name)

