#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConnectionModel(object):

    # -------------------------------------------------------------------------
    def __init__(self, diagram, output, output_port, conn_type):
        self.output = output
        self.output_port = output_port
        self.conn_type = conn_type
        self.input = None
        self.input_port = -1
        self.diagram = diagram

# -----------------------------------------------------------------------------
