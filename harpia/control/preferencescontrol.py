# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

from harpia.utils.XMLUtils import XMLParser
import os
import ast

class PreferencesControl():

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
                try:
                    self.hp.set_recent_files(ast.literal_eval(prop.getAttr("value")))
                except:
                    pass
            if prop.getAttr("name") == "default_directory":
                self.hp.set_default_directory(prop.getAttr("value"))
            if prop.getAttr("name") == "error_log_file":
                self.hp.set_error_log_file(prop.getAttr("value"))
            if prop.getAttr("name") == "width":
                self.hp.set_width(int(prop.getAttr("value")))
            if prop.getAttr("name") == "height":
                self.hp.set_height(int(prop.getAttr("value")))
            if prop.getAttr("name") == "hpaned_work_area":
                self.hp.set_hpaned_work_area(int(prop.getAttr("value")))
            if prop.getAttr("name") == "vpaned_bottom":
                self.hp.set_vpaned_bottom(int(prop.getAttr("value")))
            if prop.getAttr("name") == "vpaned_left":
                self.hp.set_vpaned_left(int(prop.getAttr("value")))
        return True

    # ----------------------------------------------------------------------
    def save(self):
        conf = "<HarpiaProperties>\n"
        conf += "<property name='recent_files' value=\"" + str(map(str, self.hp.get_recent_files())) + "\"/>\n"
        conf += "<property name='default_directory' value='" + self.hp.get_default_directory() + "'/>\n"
        conf += "<property name='error_log_file' value='" + self.hp.get_error_log_file() + "'/>\n"
        conf += "<property name='width' value='" + str(self.hp.get_width()) + "'/>\n"
        conf += "<property name='height' value='" + str(self.hp.get_height()) + "'/>\n"
        conf += "<property name='hpaned_work_area' value='" + str(self.hp.get_hpaned_work_area()) + "'/>\n"
        conf += "<property name='vpaned_bottom' value='" + str(self.hp.get_vpaned_bottom()) + "'/>\n"
        conf += "<property name='vpaned_left' value='" + str(self.hp.get_vpaned_left()) + "'/>\n"
        conf += "</HarpiaProperties>\n"

        try:
            confFile = file(os.path.expanduser(self.hp.conf_file_path), 'w')
            confFile.write(conf)
            confFile.close()
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------

