# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PreferencesPersistence class.
"""
import os
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.model.preferences import Preferences

tag_name = "MosaicodeProperties"


class PreferencesPersistence:
    """
    This class contains methods related the PreferencesPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, path):
        """
        This method loads the diagram.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        prefs = Preferences()
        file_name = path + "/" + prefs.conf_file_path
        file_name = os.path.expanduser(file_name)
        if os.path.exists(file_name) is False:
            return prefs
        parser = XMLParser(file_name)

        if parser.getTag(tag_name) is None:
            return prefs

        try:
            prefs.default_directory = parser.getTagAttr(tag_name, "default_directory")
            prefs.default_filename = parser.getTagAttr(tag_name, "default_filename")
            prefs.grid = int(parser.getTagAttr(tag_name,"grid"))
            prefs.port = int(parser.getTagAttr(tag_name, "network_port"))
            prefs.width = int(parser.getTagAttr(tag_name,"width"))
            prefs.height = int(parser.getTagAttr(tag_name, "height"))
            prefs.hpaned_work_area = int(parser.getTagAttr(tag_name, "hpaned_work_area"))
            prefs.vpaned_bottom = int(parser.getTagAttr(tag_name, "vpaned_bottom"))
            prefs.vpaned_left = int(parser.getTagAttr(tag_name, "vpaned_left"))

            files = parser.getTag(tag_name).getTag(
                        "recent_files").getChildTags("name")
            for file_name in files:
                prefs.recent_files.append(file_name.getAttr("value"))
        except:
            pass
        return prefs

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, prefs, path):
        """
        This method save the diagram.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        parser = XMLParser()
        parser.addTag(tag_name)
        parser.setTagAttr(tag_name,'default_directory', prefs.default_directory)
        parser.setTagAttr(tag_name,'default_filename', prefs.default_filename)
        parser.setTagAttr(tag_name,'grid', prefs.grid)
        parser.setTagAttr(tag_name, 'network_port', prefs.port)
        parser.setTagAttr(tag_name,'width', prefs.width)
        parser.setTagAttr(tag_name,'height', prefs.height)
        parser.setTagAttr(tag_name,'hpaned_work_area', prefs.hpaned_work_area)
        parser.setTagAttr(tag_name,'vpaned_bottom', prefs.vpaned_bottom)
        parser.setTagAttr(tag_name,'vpaned_left', prefs.vpaned_left)

        parser.appendToTag(tag_name, 'recent_files')
        for key in prefs.recent_files:
            parser.appendToTag('recent_files', 'name', value=key)

        try:
            file_name = path + "/" + prefs.conf_file_path
            confFile = file(os.path.expanduser(file_name), 'w')
            confFile.write(parser.prettify())
            confFile.close()
        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------
