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
    def add_block(self, block):
        if self.language is not None and self.language != block.language:
            System.log("Block language is different from diagram language.")
            return False
        if self.language is None or self.language == 'None':
            self.language = block.language

        self.last_id = max(int(self.last_id), int(block.id))
        if block.id < 0:
            block.id = self.last_id
        self.blocks[block.id] = block
        self.last_id += 1
        return True

# ----------------------------------------------------------------------
