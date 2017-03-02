#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConnectionModel(object):

    # -------------------------------------------------------------------------
    def __init__(self, diagram, source, source_port, conn_type):
        self.source = source
        self.source_port = source_port
        self.conn_type = conn_type
        self.sink = None
        self.sink_port = -1
        self.__diagram = diagram

    # -------------------------------------------------------------------------
    def get_diagram(self):
        return self.__diagram

    # -------------------------------------------------------------------------
    def type_match(self):
        outType = self.source.get_out_ports()[int(self.source_port)]["type"]
        inType = self.sink.get_in_ports()[int(self.sink_port)]["type"]
        return outType == inType

    # ----------------------------------------------------------------------
    def set_end(self, sink, sink_port):
        self.sink = sink
        self.sink_port = sink_port

# -----------------------------------------------------------------------------
