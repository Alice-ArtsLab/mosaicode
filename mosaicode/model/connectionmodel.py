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
        self.diagram = diagram

# -----------------------------------------------------------------------------
