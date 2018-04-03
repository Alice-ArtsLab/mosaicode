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
from mosaicode.system import System as System


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
        self.old_path = os.path.realpath(os.curdir)

        self.blockList = []
        self.connections = []
        self.codes = {}

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

    # ----------------------------------------------------------------------
    def __replace_wildcards(self, text):
        """
        This method replace the wildcards.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        result = text.replace("%t", str(time.time()))
        date = datetime.datetime.now().strftime("(%Y-%m-%d-%H:%M:%S)")
        result = result.replace("%d", date)
        result = result.replace("%l", self.diagram.language)
        result = result.replace("%n", self.diagram.patch_name)
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
        name = self.__replace_wildcards(name)
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
        name = self.__replace_wildcards(name)
        return name

    # ----------------------------------------------------------------------
    def __prepare_block_list(self):
        """
        This method prepare the blocks to code generation.
        """
        for block_key in self.diagram.blocks:
            block = self.diagram.blocks[block_key]
            # Creating class attributes on the fly
            try:
                block.weight = 0
            except:
                block.__class__.weight = 0
            try:
                block.connections = []
            except:
                block.__class__.connections = []

            # Listing all connections that the block is output
            for connection in self.diagram.connectors:
                if connection.output != block:
                    continue
                block.connections.append(connection)
            self.blockList.append(block)

    # ----------------------------------------------------------------------
    def __sort_block_list(self):
        """
        This method sorts the blocks to code generation.
        """
        # adjust the weight of every blocks depending on the connection net
        modification = True
        while modification:
            modification = False
            for block in self.blockList:
                for connection in block.connections:
                    for block_target in self.blockList:
                        if block_target != connection.input:
                            continue
                        weight = block.weight
                        if block_target.weight < weight + 1:
                            block_target.weight = weight + 1
                            modification = True

    # ----------------------------------------------------------------------
    def __generate_block_list_code(self):
        """
        This method interacts block by block to generate all code.
        """
        active_weight = 0
        # The maxWeight is, in the worst case, the block list lenght
        max_weight = len(self.blockList)
        while active_weight <= max_weight:
            if len(self.blockList) == 0:
                break
            for block in self.blockList:
                if block.weight == active_weight:
                    # If it your time, lets generate your code and remove you
                    self.__generate_block_code(block)
            active_weight += 1

    # ----------------------------------------------------------------------
    def __generate_port_var_name_code(self, block, port):
        """
        This method generate the block code.
        """
        value = port.var_name

        # Replace all port[stuff] values
        for attribute in port.__dict__:
            my_key = "$port[" + attribute + "]$"
            my_value = str(port.__dict__[attribute])
            my_value = my_value.replace(" ", "_")
            my_value = my_value.lower()
            value = value.replace(my_key,my_value)

        # Replace all block[stuff] values
        for attribute in block.__dict__:
            my_key = "$block[" + attribute + "]$"
            my_value = str(block.__dict__[attribute])
            my_value = my_value.replace(" ", "_")
            my_value = my_value.lower()
            value = value.replace(my_key, my_value)

        return value

    # ----------------------------------------------------------------------
    def __generate_block_code(self, block):
        """
        This method generate the block code.
        """

        # Empty the previous generated codes, if exist
        block.gen_codes = {}

        # For each code part, we need to replace wildcards
        for key in block.codes:
            block.gen_codes[key] = block.codes[key]

            # First we replace in ports
            for port in block.ports:
                my_key = "$port[" + port.name + "]$"
                my_value = self.__generate_port_var_name_code(block, port)
                block.gen_codes[key] = block.gen_codes[key].replace(my_key, my_value)

            # Then we replace object attributes by their values
            for attribute in block.__dict__:
                my_key = "$" + attribute + "$"
                value = str(block.__dict__[attribute])
                block.gen_codes[key] = block.gen_codes[key].replace(my_key, value)

            # Then we replace properties by their values
            for prop in block.get_properties():
                my_key = "$prop[" + prop.get("name") + "]$"
                value = str(prop.get("value"))
                block.gen_codes[key] = block.gen_codes[key].replace(my_key, value)

        # Append it all to Generator Codes
        for key in self.codes:
            if key in block.codes:
                self.codes[key].append(block.gen_codes[key])
            else:
                self.codes[key].append('')

        connections = ""
        for connection in block.connections:
            connection_code = connection.output_port.code
            # Replace output
            value = self.__generate_port_var_name_code(connection.output, connection.output_port)
            connection_code = connection_code.replace("$output$", value)

            # Replace Input
            value = self.__generate_port_var_name_code(connection.input, connection.input_port)
            connection_code = connection_code.replace("$input$", value)
            connections += connection_code

        self.connections.append(connections)


    # ----------------------------------------------------------------------
    def generate_code(self):
        """
        This method generate the source code.
        """

        System.log("Generating Code")
        self.__prepare_block_list()
        self.__sort_block_list()

        # Create an array of codes to each code part
        for key in self.code_template.code_parts:
            self.codes[key] = []

        self.__generate_block_list_code()

        code = self.code_template.code

        for key in self.codes:
            # Check for single_code generation
            code_name = "$single_code["+ key + "]$"
            if code_name in code:
                temp_header = []
                temp_code = ""
                for header_code in self.codes[key]:
                    if header_code not in temp_header:
                        temp_header.append(header_code)
                for header_code in temp_header:
                    temp_code += header_code
                code = code.replace(code_name, temp_code)
            # Check for code generation
            code_name = "$code["+ key + "]$"
            if code_name in code:
                temp_code = ""
                for x in self.codes[key]:
                    temp_code += x
                code = code.replace(code_name, temp_code)
            # Check for code + connections generation
            code_name = "$code["+ key + ", connection]$"
            if code_name in code:
                temp_code = ""
                for x,y in zip(self.codes[key], self.connections):
                    temp_code += x
                    temp_code += y
                code = code.replace(code_name, temp_code)

            # Check for connections + code generation
            code_name = "$code[connection, "+ key + "]$"
            if code_name in code:
                temp_code = ""
                for x,y in zip(self.connections, self.codes[key]):
                    temp_code += x
                    temp_code += y
                code = code.replace(code_name, temp_code)

        # Replace only connection
        connection_block = ""
        for conn in self.connections:
            connection_block += conn + "\n"
        code = code.replace("$connections$", connection_block)

        return code

    # ----------------------------------------------------------------------
    def save_code(self, name=None, code=None):
        """
        This method generate the save log.
        """
        if name is None:
            name = self.dir_name + self.filename + self.code_template.extension
            try:
                os.makedirs(self.dir_name)
            except:
                pass
        System.log("Saving Code to " + name)
        try:
            codeFile = open(name, 'w')

            if code is None:
                code = self.generate_code()
            codeFile.write(code)
            codeFile.close()
            return False
        except IOError:
            System.log("File or directory not found!")
            return True



    # ----------------------------------------------------------------------
    def run(self, code = None):
        """
        This method runs the code.
        """
        command = self.code_template.command
        command = command.replace("$filename$", self.filename)
        command = command.replace("$extension$", self.code_template.extension)
        command = command.replace("$dir_name$", self.dir_name)

        if (self.save_code(code = code)):
            System.log("Please, save the diagram!")
            return
        os.chdir(self.dir_name)

        System.log("Executing Code: " + command)

        program = Thread(target=os.system, args=(command,))
        program.start()

        while program.isAlive():
            program.join(0.4)
            while Gtk.events_pending():
                Gtk.main_iteration()
        os.chdir(self.old_path)

# -------------------------------------------------------------------------
