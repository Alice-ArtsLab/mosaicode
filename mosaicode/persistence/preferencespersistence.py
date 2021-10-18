# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PreferencesPersistence class.
"""
import os
from mosaicode.model.preferences import Preferences
from mosaicode.persistence.persistence import Persistence
import json

class PreferencesPersistence:
    """
    This class contains methods related the PreferencesPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, path):
        """
        This method loads the port from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        prefs = Preferences()
        file_name = path + "/" + prefs.conf_file_path + ".json"
        file_name = os.path.expanduser(file_name)
        if os.path.exists(file_name) is False:
            return prefs


        # load the port
        if os.path.exists(file_name) is False:
            return None

        data = ""
        try:
            data_file = open(file_name, 'r')
            data = json.load(data_file)
            data_file.close()

            if data["data"] != "PREFERENCES":
                return None

            prefs.author = data["author"]
            prefs.license = data["license"]
            prefs.version = data["version"]

            prefs.default_directory = data["default_directory"]
            prefs.default_filename = data["default_filename"]
            prefs.grid = int(data["grid"])
            prefs.port = int(data["network_port"])
            prefs.width = int(data["width"])
            prefs.height = int(data["height"])
            prefs.hpaned_work_area = int(data["hpaned_work_area"])
            prefs.vpaned_bottom = int(data["vpaned_bottom"])
            prefs.vpaned_left = int(data["vpaned_left"])

            files = data["recent_files"]
            for file_name in files:
                prefs.recent_files.append(file_name)

        except:
            from mosaicode.system import System as System
            System.log("Problem loading preferences")

        return prefs

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, prefs, path):
        """
        This method save the port in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        x = {
        'data': "PREFERENCES",
        'author': prefs.author,
        'license': prefs.license,
        'version': prefs.version,
        'default_directory': prefs.default_directory,
        'default_filename': prefs.default_filename,
        'grid': prefs.grid,
        'network_port': prefs.port,
        'width': prefs.width,
        'height': prefs.height,
        'hpaned_work_area': prefs.hpaned_work_area,
        'vpaned_bottom': prefs.vpaned_bottom,
        'vpaned_left': prefs.vpaned_left,
        'recent_files':[]
        }
        
        for key in prefs.recent_files:
            x['recent_files'].append(key)

        if not Persistence.create_dir(path):
            return False
        try:
            file_name = path + "/" + prefs.conf_file_path + ".json"
            data_file = open(file_name, 'w')
            data_file.write(json.dumps(x, indent=4))
            data_file.close()

        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------

