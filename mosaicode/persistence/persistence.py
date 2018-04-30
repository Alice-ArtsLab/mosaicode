# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the Persistence class.
"""
import os


class Persistence():
    """
    This class contains methods related the Persistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def create_dir(cls, path):
        """
        This method creates directory structure

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if os.path.isdir(path):
            return True
        try:
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                    return True
                except:
                    return False
        except IOError as e:
            return False
        return True
