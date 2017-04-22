#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the WebaudioPlugin class.
"""
from harpia.model.plugin import Plugin


class WebaudioPlugin(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.language = "javascript"
        self.framework = "webaudio"
