# -*- coding: utf-8 -*-

from harpia.model.connectionmodel import ConnectionModel as ConnectionModel
from harpia.system import System as System

class DiagramModel(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.last_id = 1  # first block is n1, increments to each new block
        self.blocks = {}  # GUI blocks
        self.connectors = []
        self.zoom = 1.0  # pixels per unit
        self.file_name = "Untitled"
        self.modified = False
        self.language = None

        self.undo_stack = []
        self.redo_stack = []

    # ----------------------------------------------------------------------
    @property
    def patch_name(self):
        return self.file_name.split("/").pop()

# ----------------------------------------------------------------------
