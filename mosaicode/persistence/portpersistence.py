# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortPersistence class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import json
from os.path import join
from mosaicode.model.port import Port
from mosaicode.persistence.persistence import Persistence


class PortPersistence():
    """
    This class contains methods related the PortPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the port from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the port
        if os.path.exists(file_name) is False:
            return None

        data = ""
        port = Port()

        try:
            data_file = open(file_name, 'r')
            data = json.load(data_file)
            data_file.close()

            if data["data"] != "PORT":
                return None

            port = Port()
            port.type = data["type"]
            port.version = data["version"]
            port.type = data["type"]
            port.language = data["language"]
            port.hint = data["hint"]
            port.color = data["color"]
            port.multiple = bool(data["multiple"])
            port.var_name = data["var_name"]
            port.code = data["code"]
        except:
            return None

        if port.type == "":
            return None

        return port

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, port, path):
        """
        This method save the port in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        x = {
          "source": "JSON",
          "data": "PORT",
          "version": port.version,
          "type": port.type,
          "language": port.language,
          "hint": port.hint,
          "color": port.color,
          "multiple": port.multiple,
          "var_name": port.var_name,
          "code": port.code
        }
        
        if not Persistence.create_dir(path):
            return False
        try:
            data_file = open(os.path.join(path, port.type + '.json'), 'w')
            data_file.write(json.dumps(x, indent=4))
            data_file.close()

        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------
