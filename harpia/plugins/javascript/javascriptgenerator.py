# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2004 - 2006 Christian Silvano (christian.silvano@gmail.com),
# Mathias Erdtmann (erdtmann@gmail.com), S2i (www.s2i.das.ufsc.br)
#            2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br),
# Clovis Peruchi Scotti(scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias
# Erdtmann(erdtmann@gmail.com) and S2i(www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
# S2i(www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this
#    software.
#
# ----------------------------------------------------------------------
import os
import webbrowser  # to open HTML file

from harpia.control.codegenerator import CodeGenerator


class JavascriptGenerator(CodeGenerator):

    # ----------------------------------------------------------------------
    def __init__(self, diagram=None):
        CodeGenerator.__init__(self, diagram)
        self.connectors = {
            "HRP_WEBAUDIO_SOUND": {
                "icon_in": "images/conn_sound_in.png",
                "icon_out": "images/conn_sound_out.png",
                "multiple": True,
                "code": 'block_$source$.connect(' +
                'block_$sink$_i[$sink_port$])\n'
            },
            "HRP_WEBAUDIO_FLOAT": {
                "icon_in": "images/conn_float_in.png",
                "icon_out": "images/conn_float_out.png",
                "multiple": True,
                "code": 'block_$source$_o$source_port$.push(' +
                'block_$sink$_i[$sink_port$])\n'
            },
            "HRP_WEBAUDIO_CHAR": {
                "icon_in": "images/conn_char_in.png",
                "icon_out": "images/conn_char_out.png",
                "multiple": True,
                "code": 'block_$source$_o$source_port$.push(' +
                'block_$sink$_i[$sink_port$])\n'
            }
        }

    # ----------------------------------------------------------------------
    def generate_code(self):
        CodeGenerator.generate_code(self)
        self.sort_blocks()
        self.generate_parts()

        header = r"""<html>
<head>
<meta http-equiv="Cache-Control" content="no-store" />
</head>
<body>
<script>

var context = new (window.AudioContext || window.webkitAudioContext)();
"""
        # Adds only if it does not contains
        temp_header = []
        for header_code in self.headers:
            if header_code not in temp_header:
                temp_header.append(header_code)

        for header_code in temp_header:
            header += header_code

        declaration_block = "\n//declaration block\n"

        for var in self.declarations:
            declaration_block += var

        declaration_block += "\n//connections\n"

        for conn in self.connections:
            declaration_block += conn

        execution = "\n\t//execution block\n"
        for x in self.functionCalls:
            execution += x

        execution += "</script>\n"

        deallocating = "\n<! deallocation block --!>\n"
        for x in self.deallocations:
            deallocating += x

        closing = ""
        closing += "\n"
        for outDea in self.outDeallocations:
            closing += outDea

        closing += "</body>\n</html>"

        # Final code assembly
        return header + declaration_block + execution + deallocating + closing

    # ----------------------------------------------------------------------
    def save_code(self):
        CodeGenerator.save_code(self)
        self.change_directory()
        codeFile = open(self.filename + '.html', 'w')
        code = self.generate_code()
        codeFile.write(code)
        codeFile.close()
        self.return_to_old_directory()

    # ----------------------------------------------------------------------
    def compile(self):
        self.save_code()

    # ----------------------------------------------------------------------
    def execute(self):
        CodeGenerator.execute(self)
        self.compile()
        self.change_directory()
        result = webbrowser.open_new(self.filename + '.html')
        self.return_to_old_directory()

# -------------------------------------------------------------------------
