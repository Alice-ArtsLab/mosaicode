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
            self.inherited_classes = None
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

    # ----------------------------------------------------------------------
    def getDependencies(self):
        dependencies = ''
        if self.dependencies != None:
            for dependency in self.dependencies:
                dependencies += 'from '+dependency['from']+ ' import ' +dependency['import']+ '\n'

        dependencies += '\n'
        return dependencies

    # ----------------------------------------------------------------------
    def getInheritedClasses(self):
        if self.inherited_classes is None:
            return '(object):'
        inherited_classes = '('
        for inherit in self.inherited_classes:
            inherited_classes += inherit + ', '
        inherited_classes = inherited_classes[:len(inherited_classes)-2]
        inherited_classes += '):'
        return inherited_classes

    # ----------------------------------------------------------------------
    def clear_string(self, string):
        start = 0
        end = len(string)
        if end == 0:
            return 0
        while (string[start] == '\n' or string[start] == ' '):
            start += 1
            if start == len(string):
                break
        while (string[end-1] == '\n' or string[end-1] == ' '):
            end -= 1
            if end == 0:
                break
        string = string[start:end]

        return string

    # ----------------------------------------------------------------------
    def save(self, file_name):
        space = '    '
        f = file(os.path.expanduser(file_name), 'w')
        source = '#!/usr/bin/env python\n' + '# -*- coding: utf-8 -*-\n'
        source += self.getDependencies()
        source += 'class ' + self.class_name + self.getInheritedClasses()+'\n'
        source+= space + 'def __init__(self):\n'
        for attr in self.attributes:
            string = str(self.attributes[str(attr)])
            string = str(self.clear_string(string))
            if type(self.attributes[attr]) is not (type([]) or type({})):
                string = '\'\'\''+ string+ '\'\'\''
            source += space*2+ 'self.'+str(attr)+ ' = '+ string + '\n'

        f.write(source)
        f.close()

# ----------------------------------------------------------------------
