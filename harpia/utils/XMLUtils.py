from bs4 import BeautifulSoup


class XMLParser(object):


    def __init__(self, source=None, fromString=False, fromTag=False):

        if (source is None):
            #self.parsedXML = BeautifulSoup(features='xml')
            self.__dict__['parsedXML'] = BeautifulSoup(features='xml')
        elif fromString:
            #self.parsedXML = BeautifulSoup(source, "xml")
            self.__dict__['parsedXML'] = BeautifulSoup(source, "xml")
        elif fromTag:
            self.__dict__['parsedXML'] = source;
            #self.parsedXML = source
        else:
            #self.parsedXML = BeautifulSoup(open(source), "xml")
            self.__dict__['parsedXML'] = BeautifulSoup(open(source), "xml")

    def getTagAttr(self, tag, attr):
        return getattr(self.parsedXML, tag)[attr]

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

    def addTag(self, tagName, attrs):
        self.parsedXML.append(self.parsedXML.new_tag(tagName, **attrs))

    def appendToTag(self, tagParent, tagChild, attrs):
        getattr(self.parsedXML, tagParent).append(self.parsedXML.new_tag(tagChild, **attrs))

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

    def __repr__(self):
        return str(self.parsedXML)

    def __getattr__(self, attr):
        #print type(self.parsedXML)
        return self.parsedXML[attr]

    def __setattr__(self, attr, value):
        self.parsedXML[attr] = value


    # __str__ is the same as __repr__
    __str__ = __repr__
