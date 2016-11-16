#!/usr/bin/env python
# -*- coding: utf-8 -*-
from harpia.model.plugin import Plugin


class WebaudioPlugin(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.language = "javascript"
