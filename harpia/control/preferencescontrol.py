# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import os
from harpia.utils.XMLUtils import XMLParser


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
        if os.path.exists(file_name) is False:
            return
        xml_loader = XMLParser(file_name)
        properties = xml_loader.getTag(
            "HarpiaProperties").getChildTags("property")

        for prop in properties:
            if prop.getAttr("name") in self.hp.__dict__:
                self.hp.__dict__[prop.getAttr("name")] = prop.getAttr("value")
        return True

    # ----------------------------------------------------------------------
    def save(self):
        conf = "<HarpiaProperties>\n"
        for key in self.hp.__dict__:
            conf += "<property name='" + key + "' value=\"" + \
                str(self.hp.__dict__[key]) + "\"/>\n"
        conf += "</HarpiaProperties>\n"

        try:
            confFile = file(os.path.expanduser(self.hp.conf_file_path), 'w')
            confFile.write(conf)
            confFile.close()
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
