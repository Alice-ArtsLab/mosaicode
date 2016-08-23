# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

from harpia.utils.XMLUtils import XMLParser
import os


class HarpiaPropertiesControl():

    # ----------------------------------------------------------------------
    def __init__(self, harpia_properties):
        self.hp = harpia_properties

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def load(self):
        # load the diagram
        file_name = os.path.expanduser(self.hp.conf_file_path)
        if os.path.exists(file_name) == False:
            return
        xml_loader = XMLParser(file_name)
        properties = xml_loader.getTag("HarpiaProperties").getChildTags("property")

        for prop in properties:
            if prop.getAttr("name") == "recent_files":
                self.hp.set_recent_files(list(prop.getAttr("value")))
            if prop.getAttr("name") == "default_directory":
                self.hp.set_default_directory(prop.getAttr("value"))
            if prop.getAttr("name") == "error_log_file":
                self.hp.set_error_log_file(prop.getAttr("value"))
        return True

    # ----------------------------------------------------------------------
    def save(self):
        conf = "<HarpiaProperties>\n"
        conf += "<property name='recent_files' value='" + str(self.hp.get_recent_files()) + "'/>\n"
        conf += "<property name='default_directory' value='" + self.hp.get_default_directory() + "'/>\n"
        conf += "<property name='error_log_file' value='" + self.hp.get_error_log_file() + "'/>\n"
        conf += "</HarpiaProperties>\n"

        try:
            confFile = file(os.path.expanduser(self.hp.conf_file_path), 'w')
            confFile.write(conf)
            confFile.close()
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------

