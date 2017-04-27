# -*- coding: utf-8 -*-
"""
This module contains the PythonParser class.
"""
import os

class PythonParser(object):
    """
    This class contains methods related the PythonParser class.
    """
    # ----------------------------------------------------------------------
    def __init__(self, file_name=None):
        if file_name is None:
            self.class_name = None
            self.dependencies = None
            self.attributes = {}
        else:
            self.__load()


    # ----------------------------------------------------------------------
    def __load(self):
        pass

    # ----------------------------------------------------------------------
    def setAttribute(self, attr, value):
        self.attributes[attr] = value

    # ----------------------------------------------------------------------
    def getAttributeValue(self, attr):
        try:
            return self.attributes[attr]
        except:
            print "Attribute", attr,"doesn\'t exist!"
            return None
    def getDependencies(self):
        if self.dependencies is None:
            return '(object):'
        dependencies = '('
        for dependency in self.dependencies:
            dependencies += dependency + ', '
        dependencies = dependencies[:len(dependencies)-2]
        dependencies += '):'
        return dependencies
    # ----------------------------------------------------------------------
    def save(self, file_name):
        space = '    '
        f = file(os.path.expanduser(file_name), 'w')
        source = '#!/usr/bin/env python\n' + '# -*- coding: utf-8 -*-\n'
        source += 'class ' + self.class_name + self.getDependencies()+'\n'

        for attr in self.attributes:
            string = str(self.attributes[str(attr)])
            start = 0
            end = len(string)
            while (string[start] == '\n' or string[start] == ' '):
                start += 1
                if start == len(string):
                    break
            while (string[end-1] == '\n' or string[end-1] == ' '):
                end -= 1
                if end == 0:
                    break

            string = string[start:end]
            if type(self.attributes[attr]) is not type([]):
                string = '\''+ string+ '\''

            source += space+ 'self.'+str(attr)+ ' = '+ string + '\n'

        f.write(source)
        f.close()
# ----------------------------------------------------------------------
