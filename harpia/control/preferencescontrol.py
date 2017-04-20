# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PreferencesControl class.
"""
import os
import ast
from harpia.utils.XMLUtils import XMLParser
from harpia.model.preferences import Preferences

class PreferencesControl():
    """
    This class contains methods related the PreferencesControl class.
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
        from harpia.system import System
        file_name = System.get_user_dir() + "/" + prefs.conf_file_path
        file_name = os.path.expanduser(file_name)
        if os.path.exists(file_name) is False:
            return
        parser = XMLParser(file_name)

        if parser.getTag("HarpiaProperties") is None:
            return None

        try:
            prefs.default_directory = parser.getTagAttr("HarpiaProperties",
                        "default_directory")
            prefs.default_filename = parser.getTagAttr("HarpiaProperties",
                        "default_filename")
            prefs.error_log_file = parser.getTagAttr("HarpiaProperties",
                        "error_log_file")
            prefs.grid = int(parser.getTagAttr("HarpiaProperties","grid"))
            prefs.width = int(parser.getTagAttr("HarpiaProperties","width"))
            prefs.height = int(parser.getTagAttr("HarpiaProperties",
                        "height"))
            prefs.hpaned_work_area = int(parser.getTagAttr("HarpiaProperties",
                        "hpaned_work_area"))
            prefs.vpaned_bottom = int(parser.getTagAttr("HarpiaProperties",
                        "vpaned_bottom"))
            prefs.vpaned_left = int(parser.getTagAttr("HarpiaProperties",
                        "vpaned_left"))

            files = parser.getTag("HarpiaProperties").getTag(
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
        parser.addTag('HarpiaProperties')
        parser.setTagAttr('HarpiaProperties','default_directory',
                prefs.default_directory)
        parser.setTagAttr('HarpiaProperties','default_filename',
                prefs.default_filename)
        parser.setTagAttr('HarpiaProperties','error_log_file',
                prefs.error_log_file)
        parser.setTagAttr('HarpiaProperties','grid', prefs.grid)
        parser.setTagAttr('HarpiaProperties','width', prefs.width)
        parser.setTagAttr('HarpiaProperties','height', prefs.height)
        parser.setTagAttr('HarpiaProperties','prefsaned_work_area',
                prefs.hpaned_work_area)
        parser.setTagAttr('HarpiaProperties','vpaned_bottom',
                prefs.vpaned_bottom)
        parser.setTagAttr('HarpiaProperties','vpaned_left',
                prefs.vpaned_left)

        parser.appendToTag('HarpiaProperties', 'recent_files')
        for key in prefs.recent_files:
            parser.appendToTag('recent_files', 'name', value=key)

        try:
            from harpia.system import System
            file_name = System.get_user_dir() + "/" + prefs.conf_file_path
            confFile = file(os.path.expanduser(file_name), 'w')
            confFile.write(parser.prettify())
            confFile.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_recent_file(cls, prefs, file_name):
        if file_name in prefs.recent_files:
            prefs.recent_files.remove(file_name)
        prefs.recent_files.insert(0, file_name)
        if len(prefs.recent_files) > 10:
            prefs.recent_files.pop()

# ----------------------------------------------------------------------
