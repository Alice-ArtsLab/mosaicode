# -*- coding: utf-8 -*-
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
        if self.parsedXML.find(tag):
            return XMLParser(getattr(self.parsedXML, tag), fromTag=True)
        else:
            return None

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
