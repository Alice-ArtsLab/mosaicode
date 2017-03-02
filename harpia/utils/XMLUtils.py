# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
# S2i (www.s2i.das.ufsc.br)
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
#    For further information, check the COPYING file distributed with
#    this software.
#
# ----------------------------------------------------------------------
"""
This module contains the XMLParser class.
"""
from bs4 import BeautifulSoup


class XMLParser(object):
    """
    This class contains methods related the XMLParser class.
    """

    def __init__(self, source=None, fromString=False, fromTag=False):

        if (source is None):
            self.__dict__['parsedXML'] = BeautifulSoup(features='xml')
        elif fromString:
            self.__dict__['parsedXML'] = BeautifulSoup(source, "xml")
        elif fromTag:
            self.__dict__['parsedXML'] = source
        else:
            self.__dict__['parsedXML'] = BeautifulSoup(open(source),
                                                       "xml",
                                                       from_encoding="UTF-8")

    def getTagAttr(self, tag, attr):
        return getattr(self.parsedXML, tag)[attr]

    def setTagAttr(self, tag, attr, value):
        getattr(self.parsedXML, tag)[attr] = value

    def getAttr(self, attr):
        return self.parsedXML[attr]

    def setAttr(self, attr, value):
        self.parsedXML[attr] = value

    def getChildTagAttr(self, parent, child, attr):
        return getattr(getattr(self.parsedXML, parent), child)[attr]

    def setChildTagAttr(self, parent, child, attr, value):
        getattr(getattr(self.parsedXML, parent), child)[attr] = value

    def getChildTags(self, child):
        tags = []
        for tag in self.parsedXML.find_all(child):
            tags.append(XMLParser(tag, fromTag=True))
        return tags

    def addTag(self, tagName, **attrs):
        new_tag = self.parsedXML.new_tag(tagName, **attrs)
        self.parsedXML.append(new_tag)
        return new_tag

    def appendToTag(self, tagParent, tagChild, **attrs):
        new_tag = self.parsedXML.new_tag(tagChild, **attrs)
        getattr(self.parsedXML, tagParent).append(new_tag)
        return new_tag

    def appendToLastTag(self, tagParent, tagChild, **attrs):
        new_tag = self.parsedXML.new_tag(tagChild, **attrs)
        self.parsedXML.find_all(tagParent)[-1].append(new_tag)
        return new_tag

    def getXML(self):
        return self.parsedXML.prettify()

    def getTagXML(self, tag):
        return tag.prettify()

    def getTag(self, tag):
        return XMLParser(getattr(self.parsedXML, tag), fromTag=True)

    def getTagChild(self, parent, child):
        return getattr(getattr(self.parsedXML, parent), child)

    def getTagContent(self):
        return self.parsedXML.contents[0]

    def getTagChildren(self):
        return self.parsedXML.children

    def getText(self):
        return self.parsedXML.text

    def prettify(self):
        return self.parsedXML.prettify()

    def __repr__(self):
        return str(self.parsedXML)

    def __getattr__(self, attr):
        return self.parsedXML[attr]

    def __setattr__(self, attr, value):
        self.parsedXML[attr] = value

    # __str__ is the same as __repr__
    __str__ = __repr__
