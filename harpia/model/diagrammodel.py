#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.model.connectionmodel import ConnectionModel as ConnectionModel


class DiagramModel(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.block_id = 1  # first block is n1, increments to each new block
        self.blocks = {}  # GUI blocks
        self.connectors = []
        self.__zoom = 1.0  # pixels per unit
        self.__file_name = "Untitled"
        self.__modified = False
        self.language = None

    # ----------------------------------------------------------------------
    def add_block(self, block):
        if self.language is not None and self.language != block.get_language():
            return False
        if self.language is None or self.language == 'None':
            self.language = block.get_language()
        if block.get_id() < 0:
            block.set_id(self.block_id)
        self.blocks[int(block.get_id())] = block
        self.block_id = self.block_id + 1
        self.block_id = max(int(self.block_id), int(block.get_id()))
        return True

    # ----------------------------------------------------------------------
    def delete_block(self, block):
        if block.get_id() not in self.blocks:
            return False
        for idx in reversed(range(len(self.connectors))):
            if self.connectors[idx].source == block \
                    or self.connectors[idx].sink == block:
                self.delete_connection(self.connectors[idx])
        return True

    # ----------------------------------------------------------------------
    def add_connection(self, connection):
        self.connectors.append(connection)

    # ----------------------------------------------------------------------
    def delete_connection(self, connection):
        if connection not in self.connectors:
            return
        self.connectors.remove(connection)

    # ----------------------------------------------------------------------
    def connect_blocks(self, source, source_port, sink, sink_port):
        out_type = source.get_out_types()[source_port]
        connection = ConnectionModel(self, source, source_port, out_type)
        connection.sink = sink
        connection.sink_port = sink_port
        self.connectors.append(connection)

    # ----------------------------------------------------------------------
    def set_file_name(self, file_name):
        self.__file_name = file_name

    # ----------------------------------------------------------------------
    def get_file_name(self):
        return self.__file_name

    # ----------------------------------------------------------------------
    def get_patch_name(self):
        return self.__file_name.split("/").pop()

    # ---------------------------------------------------------------------
    def set_modified(self, state):
        self.__modified = state

    # ---------------------------------------------------------------------
    def get_modified(self):
        return self.__modified

    # ---------------------------------------------------------------------
    def set_zoom(self, zoom):
        self.__zoom = zoom

    # ---------------------------------------------------------------------
    def get_zoom(self):
        return self.__zoom
