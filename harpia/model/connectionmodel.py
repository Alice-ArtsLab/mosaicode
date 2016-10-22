#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConnectionModel(object):

    # -------------------------------------------------------------------------
    def __init__(self, diagram, source, source_port, conn_type):
        self.source = source
        self.source_port = source_port
        self.type = conn_type
        self.sink = None
        self.sink_port = -1
        self.__diagram = diagram

    # -------------------------------------------------------------------------
    def get_diagram(self):
        return self.__diagram

    # -------------------------------------------------------------------------
    def type_match(self):
        outType = self.source.get_out_types()[self.source_port]
        inType = self.sink.get_in_types()[self.sink_port]
        return outType == inType

    # -------------------------------------------------------------------------
    def get_source_port_name(self):
        return self.source.get_input_port_name(self.source_port)

    # -------------------------------------------------------------------------
    def get_sink_port_name(self):
        return self.sink.get_output_port_name(self.sink_port)

    # ----------------------------------------------------------------------
    def set_end(self, sink, sink_port):
        self.sink = sink
        self.sink_port = sink_port

# -----------------------------------------------------------------------------
