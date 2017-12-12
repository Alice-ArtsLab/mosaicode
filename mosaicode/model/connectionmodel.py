#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConnectionModel(object):

    # -------------------------------------------------------------------------
    def __init__(self, diagram, output, output_port, port):
        self.output = output
        self.output_port = output_port
        self.port = port
        self.input = None
        self.input_port = None
        self.diagram = diagram

# -----------------------------------------------------------------------------
