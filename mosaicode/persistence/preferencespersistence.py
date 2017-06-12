# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PreferencesPersistence class.
"""
import os
import ast
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.model.preferences import Preferences

class PreferencesPersistence():
    """
    This class contains methods related the PreferencesPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls):
        """
        This method loads the diagram.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        prefs = Preferences()
        from mosaicode.system import System
        file_name = System.get_user_dir() + "/" + prefs.conf_file_path
        file_name = os.path.expanduser(file_name)
        if os.path.exists(file_name) is False:
            return prefs
        parser = XMLParser(file_name)

        if parser.getTag("MosaicodeProperties") is None:
            return prefs

        try:
            prefs.default_directory = parser.getTagAttr("MosaicodeProperties",
                        "default_directory")
            prefs.default_filename = parser.getTagAttr("MosaicodeProperties",
                        "default_filename")
            prefs.grid = int(parser.getTagAttr("MosaicodeProperties","grid"))
            prefs.width = int(parser.getTagAttr("MosaicodeProperties","width"))
            prefs.height = int(parser.getTagAttr("MosaicodeProperties",
                        "height"))
            prefs.hpaned_work_area = int(parser.getTagAttr("MosaicodeProperties",
                        "hpaned_work_area"))
            prefs.vpaned_bottom = int(parser.getTagAttr("MosaicodeProperties",
                        "vpaned_bottom"))
            prefs.vpaned_left = int(parser.getTagAttr("MosaicodeProperties",
                        "vpaned_left"))

            files = parser.getTag("MosaicodeProperties").getTag(
                        "recent_files").getChildTags("name")
            for file_name in files:
                prefs.recent_files.append(file_name.getAttr("value"))
        except:
            pass
        return prefs

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, prefs):
        """
        This method save the diagram.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        parser = XMLParser()
        parser.addTag('MosaicodeProperties')
        parser.setTagAttr('MosaicodeProperties','default_directory',
                prefs.default_directory)
        parser.setTagAttr('MosaicodeProperties','default_filename',
                prefs.default_filename)
        parser.setTagAttr('MosaicodeProperties','grid', prefs.grid)
        parser.setTagAttr('MosaicodeProperties','width', prefs.width)
        parser.setTagAttr('MosaicodeProperties','height', prefs.height)
        parser.setTagAttr('MosaicodeProperties','hpaned_work_area',
                prefs.hpaned_work_area)
        parser.setTagAttr('MosaicodeProperties','vpaned_bottom',
                prefs.vpaned_bottom)
        parser.setTagAttr('MosaicodeProperties','vpaned_left',
                prefs.vpaned_left)

        parser.appendToTag('MosaicodeProperties', 'recent_files')
        for key in prefs.recent_files:
            parser.appendToTag('recent_files', 'name', value=key)

        try:
            from mosaicode.system import System
            file_name = System.get_user_dir() + "/" + prefs.conf_file_path
            confFile = file(os.path.expanduser(file_name), 'w')
            confFile.write(parser.prettify())
            confFile.close()
        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------
