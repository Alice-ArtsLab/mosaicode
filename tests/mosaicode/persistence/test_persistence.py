import os
from tests.mosaicode.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.persistence.persistence import Persistence

class PersistenceTest(TestBase):

    def test_create_dir(self):
        Persistence.create_dir(None)
        Persistence.create_dir("/etc/")
        Persistence.create_dir("/tmp/test")
        os.rmdir("/tmp/test")

