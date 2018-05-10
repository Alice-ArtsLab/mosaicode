# -*- coding: utf-8 -*-

class DiagramModel(object):
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

    # ----------------------------------------------------------------------
    def __init__(self):
        self.last_id = 1  # first block is n1, increments to each new block
        self.blocks = {}  # GUI blocks
        self.connectors = []
        self.comments = []
        self.zoom = 1.0  # pixels per unit
        self.file_name = "Untitled"
        self.modified = False
        self.language = None
        self.undo_stack = []
        self.redo_stack = []

    # ----------------------------------------------------------------------
    @property
    def patch_name(self):
        name = self.file_name.split("/").pop()
        name = name.split(".")[0]
        return name

# ----------------------------------------------------------------------
