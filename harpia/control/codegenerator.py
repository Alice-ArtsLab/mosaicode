# -*- coding: utf-8 -*-
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
        self.error_log_file = System.properties.error_log_file
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
        result = result.replace("%n", self.diagram.patch_name[:-4])
        result = result.replace(" ", "_")
        return result

    # ----------------------------------------------------------------------
    def get_dir_name(self):
        """
        This method return the directory name.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        name = System.properties.default_directory
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
        name = System.properties.default_filename
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
    def replace_key_value(self, plugin, key, value):
        i = 0
        for code in plugin.codes:
            plugin.codes[i] = code.replace(key, value)
            i += 1

    # ----------------------------------------------------------------------
    def generate_block_code(self, plugin):
        """
        This method generate the block code.
        """

#        # First we replace in ports
#        cont = 0
#        for port in plugin.in_ports:
#            my_key = "$in_ports[" + port["name"] + "]$"
#            value = System.ports[port["type"]].var_name
#            value = value.replace("$port_number$", str(cont))
#            value = value.replace("$port_name$", port["name"])
#            i = 0
#            for code in plugin.codes:
#                plugin.codes[i] = code.replace(my_key, value)
#                i += 1
#            cont += 1

#        # First we replace out ports
#        cont = 0
#        for port in plugin.out_ports:
#            my_key = "$out_ports[" + port["name"] + "]$"
#            value = System.ports[port["type"]].var_name
#            value = value.replace("$port_number$", str(cont))
#            value = value.replace("$port_name$", port["name"])
#            i = 0
#            for code in plugin.codes:
#                plugin.codes[i] = code.replace(my_key, value)
#                i += 1
#            cont += 1


        # First we replace object attributes by their values
        for key in plugin.__dict__:
            my_key = "$" + key + "$"
            value = str(plugin.__dict__[key])
            self.replace_key_value(plugin, my_key, value)

        # Then we replace properties by their values
        for prop in plugin.get_properties():
            my_key = "$prop[" + prop.get("name") + "]$"
            value = str(prop.get("value"))
            self.replace_key_value(plugin, my_key, value)

        for code, plugin_code in zip(self.codes, plugin.codes):
            code.append(plugin_code)

        connections = ""
        for x in plugin.connections:
            code = System.ports[x.conn_type].code
            # Replace all connection properties by their values
            for key in x.__dict__:
                value = str(x.__dict__[key])
                my_key = "$" + key + "$"
                code = code.replace(my_key, value)
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
            if code_name not in code:
                count = count + 1
                continue
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
            if code_name not in code:
                count = count + 1
                continue
            temp_code = ""
            for x in codex:
                temp_code += x
            code = code.replace(code_name, temp_code)
            count = count + 1

        # Replace code + connection
        count = 0
        for codex in self.codes:
            code_name = "$code["+ str(count) + ", connection]$"
            if code_name not in code:
                count = count + 1
                continue
            temp_code = ""
            for x,y in zip(codex, self.connections):
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
