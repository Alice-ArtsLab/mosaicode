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
#  Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br),
#                        Mathias Erdtmann (erdtmann@gmail.com) and
#                        S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
#                         S2i (www.s2i.das.ufsc.br)
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
import time
import datetime
import gettext
from harpia.system import System as System


# i18n
_ = gettext.gettext
gettext.bindtextdomain(System.APP, System.DIR)
gettext.textdomain(System.APP)


class CodeGenerator():

    # ----------------------------------------------------------------------

    def __init__(self, diagram=None):
        self.connectors = {}
        self.diagram = diagram
        if diagram is None:
            return

        self.diagram = diagram

        if self.diagram.language is None:
            System.log("No language, no block, no code")
            return
        self.dir_name = self.get_dir_name()
        self.filename = self.get_filename()
        self.error_log_file = System.properties.get_error_log_file()
        self.error_log_file = self.replace_wildcards(self.error_log_file)
        self.old_path = os.path.realpath(os.curdir)

        self.blockList = []
        self.outDeallocations = []
        self.functionCalls = []
        self.connections = []
        self.headers = []
        self.declarations = []
        self.deallocations = []

        if not len(self.diagram.blocks) > 0:
            System.log("Diagram is empty. Nothing to generate.")
            return

    # ----------------------------------------------------------------------
    def replace_wildcards(self, text):
        result = text.replace("%t", str(time.time()))
        date = datetime.datetime.now().strftime("(%Y-%m-%d-%H:%M:%S)")
        result = result.replace("%d", date)
        result = result.replace("%l", self.diagram.language)
        result = result.replace("%n", self.diagram.get_patch_name()[:-4])
        result = result.replace(" ", "_")
        return result

    # ----------------------------------------------------------------------
    def get_dir_name(self):
        name = System.properties.get_default_directory()
        name = self.replace_wildcards(name)
        if not name.endswith("/"):
            name = name + "/"
        return name

    # ----------------------------------------------------------------------
    def get_filename(self):
        name = System.properties.get_default_filename()
        name = self.replace_wildcards(name)
        return name

    # ----------------------------------------------------------------------
    def change_directory(self):
        try:
            os.makedirs(self.dir_name)
        except:
            pass
        os.chdir(self.dir_name)

    # ----------------------------------------------------------------------
    def return_to_old_directory(self):
        os.chdir(self.old_path)

    # ----------------------------------------------------------------------
    def sort_blocks(self):
        for block_key in self.diagram.blocks:
            block = self.diagram.blocks[block_key]

            # Creating class attributes on the fly
            try:
                block.weight = 1
            except:
                block.__class__.weight = 1
            try:
                block.connections = []
            except:
                block.__class__.connections = []

            for connection in self.diagram.connectors:
                if connection.source != block:
                    continue
                block.connections.append(connection)
            self.blockList.append(block)

        # ajusta o peso de cada bloco
        modification = True
        while modification:
            modification = False
            for block in self.blockList:
                for connection in block.connections:
                    for block_target in self.blockList:
                        if block_target != connection.sink:
                            continue
                        weight = block.weight
                        if block_target.weight < weight + 1:
                            block_target.weight = weight + 1
                            modification = True

    # ----------------------------------------------------------------------
    def get_max_weight(self):
        biggestWeight = -1
        for block in self.blockList:
            if block.weight > biggestWeight:
                biggestWeight = block.weight
        return biggestWeight

    # ----------------------------------------------------------------------
    def generate_parts(self):
        biggestWeight = self.get_max_weight()
        for activeWeight in range(biggestWeight):
            activeWeight += 1
            for block in self.blockList:
                if block.weight == activeWeight:
                    self.generate_block_code(block)

    # ----------------------------------------------------------------------
    def generate_block_code(self, block):
        plugin = block.get_plugin()
        header = plugin.generate_header()
        declaration = plugin.generate_vars()
        functionCall = plugin.generate_function_call()
        dealloc = plugin.generate_dealloc()
        outDealloc = plugin.generate_out_dealloc()

        # First we replace properties by their values
        for prop in plugin.get_properties():
            my_key = "$" + prop.get("name") + "$"
            value = str(prop.get("value"))
            header = header.replace(my_key, value)
            declaration = declaration.replace(my_key, value)
            functionCall = functionCall.replace(my_key, value)
            dealloc = dealloc.replace(my_key, value)
            outDealloc = outDealloc.replace(my_key, value)

        # Then we replace object attributes by their values
        for key in plugin.__dict__:
            value = str(plugin.__dict__[key])
            my_key = "$" + key + "$"
            header = header.replace(my_key, value)
            declaration = declaration.replace(my_key, value)
            functionCall = functionCall.replace(my_key, value)
            dealloc = dealloc.replace(my_key, value)
            outDealloc = outDealloc.replace(my_key, value)

        self.headers.append(header)
        self.declarations.append(declaration)
        self.functionCalls.append(functionCall)
        self.deallocations.append(dealloc)
        self.outDeallocations.append(outDealloc)

        connections = ""
        for x in block.connections:
            code = System.connectors[x.type]["code"]
            # Replace all connection properties by their values
            for key in x.__dict__:
                value = str(x.__dict__[key])
                my_key = "$" + key + "$"
                code = code.replace(my_key, value)
            # Replace all connection methods by their values
            for func in dir(x):
                result = ""
                try:
                    callable(getattr(x, func))
                except:
                    continue
                # if code does not have the method, we do not execute it
                key = "$" + str(func) + "$"
                if key not in code:
                    continue
                try:
                    result = getattr(x, func)()
                except:
                    continue
                code = code.replace(key, str(result))
            connections += code
        self.connections.append(connections)

    # ----------------------------------------------------------------------
    def generate_code(self):
        System.log("Parsing Code")
        return "Houston, we have a problem!"

    # ----------------------------------------------------------------------
    def save_code(self):
        System.log("Saving Code to " + self.dir_name + self.filename)

    # ----------------------------------------------------------------------
    def compile(self):
        System.log("Compiling " + self.dir_name + self.filename)
        pass

    # ----------------------------------------------------------------------
    def execute(self):
        System.log("Executing Code")
        pass

    # ----------------------------------------------------------------------
    def __set_error_log(self, error):
        if os.name == 'nt':
            Error = file(self.error_log_file, 'wb')
        else:
            Error = file(self.error_log_file, 'w')
        System.Log.log(error)
        Error.write(error)
        Error.close()

# -------------------------------------------------------------------------
