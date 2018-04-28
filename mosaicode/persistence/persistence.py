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
        try:
            if not os.path.isdir(path):
                try:
                    os.makedirs(data_dir)
                    return True
                except:
                    return False
        except IOError as e:
            return False
        return True

