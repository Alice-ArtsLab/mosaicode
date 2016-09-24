# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2004 - 2006 Christian Silvano (christian.silvano@gmail.com), Mathias Erdtmann (erdtmann@gmail.com), S2i (www.s2i.das.ufsc.br)
#            2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
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
#    For further information, check the COPYING file distributed with this software.
#
# ----------------------------------------------------------------------
import os
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.constants import *
from harpia.s2idirectory import *

# i18n
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

class CodeGenerator():

    #----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram

        self.dir_name = DIRNAME + str(time.time())
        self.old_path = os.path.realpath(os.curdir)

        self.blockList = []
        self.outDeallocations = []
        self.functionCalls = []
        self.connections = []
        self.headers = []
        self.declarations = []
        self.deallocations = []

        if not len(self.diagram.blocks) > 0:
            harpia.s2idirectory.Log.log("Diagram is empty. Nothing to generate.")
            return

    #----------------------------------------------------------------------
    def change_directory(self):
        try:
            os.makedirs(harpia.s2idirectory.properties.get_default_directory())
        except:
            pass
        os.chdir(harpia.s2idirectory.properties.get_default_directory())
        try:
            os.makedirs(self.dir_name)
        except:
            pass
        os.chdir(harpia.s2idirectory.properties.get_default_directory() + '/' + self.dir_name)

    #----------------------------------------------------------------------
    def return_to_old_directory(self):
        os.chdir(self.old_path)

    #----------------------------------------------------------------------
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
                if connection.from_block != block.get_id():
                    continue
                block.connections.append(connection)
            self.blockList.append(block)

        # ajusta o peso de cada bloco
        for block in self.blockList:
            if len(block.get_description()["InTypes"]) != 0:
                continue
            if len(block.get_description()["OutTypes"]) == 0:
                continue
            tmpList = []
            tmpList.append(block)
            organizedChain = self.apply_weights_on_connections(tmpList, self.blockList)
            while organizedChain != []:
                organizedChain = self.apply_weights_on_connections(organizedChain, self.blockList)

    #----------------------------------------------------------------------
    def generate_parts(self):
        biggestWeight = -1
        for block in self.blockList:
            if block.weight >= biggestWeight:
                biggestWeight = block.weight

        for activeWeight in range(biggestWeight):
            activeWeight += 1
            for block in self.blockList:
                if block.weight == activeWeight:
                    self.generate_block_code(block)

    #----------------------------------------------------------------------
    def generate_block_code(self, block):
        plugin = block.get_plugin()
        header = plugin.generate_header()
        declaration = plugin.generate_vars()
        functionCall = plugin.generate_function_call()
        dealloc = plugin.generate_dealloc()
        outDealloc = plugin.generate_out_dealloc()

        # Replace all object properties by their values
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
            if x.to_block == '--':
                continue
            if x.type in harpia.s2idirectory.connections:
                connections +=  harpia.s2idirectory.connections[x.type]["code"]
            connections = connections.replace("$to_block$", str(x.to_block))
            connections = connections.replace("$to_block_in$", str(int(x.to_block_in )))
            connections = connections.replace("$from_block$", str(x.from_block))
            connections = connections.replace("$from_block_out$", str(int (x.from_block_out)))

        self.connections.append(connections)

    #----------------------------------------------------------------------
    def generate_code(self):
        return ""

    #----------------------------------------------------------------------
    def save_code(self):
        pass

    #----------------------------------------------------------------------
    def compile(self):
        pass

    #----------------------------------------------------------------------
    def execute(self):
        pass

    #----------------------------------------------------------------------
    def __set_error_log(self, error):
        if os.name == 'nt':
            Error = file(harpia.s2idirectory.properties.get_error_log_file(), 'wb')
        else:
            Error = file(harpia.s2idirectory.properties.get_error_log_file(), 'w')
        harpia.s2idirectory.Log.log(error)
        Error.write(error)
        Error.close()

    #----------------------------------------------------------------------
    def apply_weights_on_connections(self, listOfBlocks, blockList):
        returnList = []
        for block in listOfBlocks:
            ##Put the connections on returnList
            for connection in block.connections:
                ##and apply the weight on this connection
                for tmp_block in blockList:
                    if tmp_block.get_id() == connection.to_block:
                        tmp_block.weight += block.weight
                        if tmp_block not in returnList:
                            returnList.append(tmp_block)
        return returnList

#-------------------------------------------------------------------------------
