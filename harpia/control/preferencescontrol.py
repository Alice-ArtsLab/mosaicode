# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PreferencesControl class.
"""
import os
from harpia.utils.XMLUtils import XMLParser


class PreferencesControl():
    """
    This class contains methods related the PreferencesControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, harpia_properties):
        self.hp = harpia_properties

    # ----------------------------------------------------------------------
    def load(self):
        """
        This method loads the diagram.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the diagram
        file_name = os.path.expanduser(self.hp.conf_file_path)
        if os.path.exists(file_name) is False:
            return
        parser = XMLParser(file_name)
        properties = parser.getTag(
            "HarpiaProperties").getChildTags("property")

        for prop in properties:
            try:
                prop.getAttr("key")
            except:
                continue
            if prop.getAttr("key") in self.hp.__dict__:
                self.hp.__dict__[prop.getAttr("key")] = prop.getAttr("value")
        return True

    # ----------------------------------------------------------------------
    def save(self):
        """
        This method save the diagram.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        parser = XMLParser()
        parser.addTag('HarpiaProperties')
        for key in self.hp.__dict__:
            parser.appendToTag('HarpiaProperties',
                               'property',
                               key=key,
                               value=self.hp.__dict__[key])
        try:
            confFile = file(os.path.expanduser(self.hp.conf_file_path), 'w')
            confFile.write(parser.prettify())
            confFile.close()
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
