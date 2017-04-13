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
"""
This module contains the CodeGenerator class.
"""
import os
import time
import datetime
import gettext
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from threading import Thread
from harpia.system import System as System

# i18n
_ = gettext.gettext
gettext.bindtextdomain(System.APP, System.DIR)
gettext.textdomain(System.APP)


class CodeGenerator():
    """
    This class contains methods related the CodeGenerator class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram=None, code_template=None):
        self.diagram = diagram
        self.code_template = code_template

        self.dir_name = ""
        self.filename = ""
        self.error_log_file = ""
        self.old_path = os.path.realpath(os.curdir)

        self.blockList = []
        self.connections = []
        self.codes=[[],[],[],[],[]]

        if diagram is None:
            return

        if code_template is None:
            return

        if self.diagram.language is None:
            System.log("No language, no block, no code")
            return

        if not len(self.diagram.blocks) > 0:
            System.log("Diagram is empty. Nothing to generate.")
            return

        self.dir_name = self.get_dir_name()
        self.filename = self.get_filename()
        self.error_log_file = System.properties.get_error_log_file()
        self.error_log_file = self.replace_wildcards(self.error_log_file)

    # ----------------------------------------------------------------------
    def replace_wildcards(self, text):
        """
        This method replace the wildcards.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        result = text.replace("%t", str(time.time()))
        date = datetime.datetime.now().strftime("(%Y-%m-%d-%H:%M:%S)")
        result = result.replace("%d", date)
        result = result.replace("%l", self.diagram.language)
        result = result.replace("%n", self.diagram.get_patch_name()[:-4])
        result = result.replace(" ", "_")
        return result

    # ----------------------------------------------------------------------
    def get_dir_name(self):
        """
        This method return the directory name.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        name = System.properties.get_default_directory()
        name = self.replace_wildcards(name)
        if not name.endswith("/"):
            name = name + "/"
        return name

    # ----------------------------------------------------------------------
    def get_filename(self):
        """
        This method return the filename

        Returns:

            * **Types** (:class:`str<str>`)
        """
        name = System.properties.get_default_filename()
        name = self.replace_wildcards(name)
        return name

    # ----------------------------------------------------------------------
    def change_directory(self):
        """
        This method change the directory.
        """
        try:
            os.makedirs(self.dir_name)
        except:
            pass
        os.chdir(self.dir_name)

    # ----------------------------------------------------------------------
    def return_to_old_directory(self):
        """
        This method return path to old directory.
        """
        os.chdir(self.old_path)

    # ----------------------------------------------------------------------
    def sort_blocks(self):
        """
        This method sorts the blocks.
        """
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
        """
        This method get max weight.

        Returns:
        
            * **Types** (:class:`int<int>`)
        """
        biggestWeight = -1
        for block in self.blockList:
            if block.weight > biggestWeight:
                biggestWeight = block.weight
        return biggestWeight

    # ----------------------------------------------------------------------
    def generate_parts(self):
        """
        This metho generate parts.
        """
        biggestWeight = self.get_max_weight()
        for activeWeight in range(biggestWeight):
            activeWeight += 1
            for block in self.blockList:
                if block.weight == activeWeight:
                    self.generate_block_code(block)

    # ----------------------------------------------------------------------
    def generate_block_code(self, plugin):
        """
        This method generate the block code.
        """
        code0 = plugin.codes[0]
        code1 = plugin.codes[1]
        code2 = plugin.codes[2]
        code3 = plugin.codes[3]
        code4 = plugin.codes[4]

        # First we replace object attributes by their values
        for key in plugin.__dict__:
            value = str(plugin.__dict__[key])
            my_key = "$" + key + "$"
            code0 = code0.replace(my_key, value)
            code1 = code1.replace(my_key, value)
            code2 = code2.replace(my_key, value)
            code3 = code3.replace(my_key, value)
            code4 = code4.replace(my_key, value)

        # Then we replace properties by their values
        for prop in plugin.get_properties():
            my_key = "$prop[" + prop.get("name") + "]$"
            value = str(prop.get("value"))
            code0 = code0.replace(my_key, value)
            code1 = code1.replace(my_key, value)
            code2 = code2.replace(my_key, value)
            code3 = code3.replace(my_key, value)
            code4 = code4.replace(my_key, value)

        self.codes[0].append(code0)
        self.codes[1].append(code1)
        self.codes[2].append(code2)
        self.codes[3].append(code3)
        self.codes[4].append(code4)

        connections = ""
        for x in plugin.connections:
            code = System.ports[x.conn_type].get_code()
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
        """
        This method generate the source code.
        """

        System.log("Generating Code")
        self.sort_blocks()
        self.generate_parts()

        code = self.code_template.code

        # Replace single code
        count = 0
        for codex in self.codes:
            code_name = "$single_code["+ str(count) + "]$"
            if code_name in code:
                temp_header = []
                temp_code = ""
                for header_code in codex:
                    if header_code.strip() not in temp_header:
                        temp_header.append(header_code.strip())
                for header_code in temp_header:
                    temp_code += header_code
                code = code.replace(code_name, temp_code)
            count = count + 1

        # Replace code
        count = 0
        for codex in self.codes:
            code_name = "$code["+ str(count) + "]$"
            if code_name in code:
                temp_code = ""
                for x in codex:
                    temp_code += x
                code = code.replace(code_name, temp_code)
            count = count + 1

        # Replace code + connection
        count = 0
        for codex in self.codes:
            code_name = "$code["+ str(count) + ", connection]$"
            if code_name in code:
                temp_code = ""
                for x,y in codex, self.connections:
                    temp_code += x
                    temp_code += y
                code = code.replace(code_name, temp_code)
            count = count + 1

        # Replace only connection
        connection_block = ""
        for conn in self.connections:
            connection_block += conn + "\n"
        code = code.replace("$connections$", connection_block)


        return code

    # ----------------------------------------------------------------------
    def save_code(self):
        """
        This method generate the save log.
        """
        System.log("Saving Code to " + \
                self.dir_name + \
                self.filename + \
                self.code_template.extension)
        self.change_directory()
        codeFile = open(self.filename + self.code_template.extension , 'w')
        code = self.generate_code()
        codeFile.write(code)
        codeFile.close()
        self.return_to_old_directory()

    # ----------------------------------------------------------------------
    def execute(self):
        """
        This method executes the code.
        """
        command = self.code_template.command
        command = command.replace("$filename$", self.filename)
        command = command.replace("$extension$", self.code_template.extension)
        command = command.replace("$dir_name$", self.dir_name)
        command = command.replace("$error_log_file$", self.error_log_file)

        self.save_code()
        self.change_directory()

        from harpia.system import System as System
        System.log("Executing Code: " + command)

        program = Thread(target=os.system, args=(command,))
        program.start()

        while program.isAlive():
            program.join(0.4)
            while Gtk.events_pending():
                Gtk.main_iteration()

        try:
            o = open("Run" + self.error_log_file, "r")
            errors = o.read()
            System.log(errors)
            o.close()
        except:
            pass
        self.return_to_old_directory()

# -------------------------------------------------------------------------
