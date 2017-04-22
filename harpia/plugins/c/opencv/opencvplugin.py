#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the OpenCVPlugin class.
"""
from harpia.model.plugin import Plugin


class OpenCVPlugin(Plugin):
    """
    This class contains methods related the OpenCVPlugin class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.language = "c"
        self.framework = "opencv"

# -----------------------------------------------------------------------------
