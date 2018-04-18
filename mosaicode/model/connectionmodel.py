#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConnectionModel(object):

    # -------------------------------------------------------------------------
    def __init__(self, diagram, output, output_port, input=None, input_port=None):
        self.output = output
        self.output_port = output_port
        self.input = input
        self.input_port = input_port
        self.diagram = diagram

# -----------------------------------------------------------------------------
