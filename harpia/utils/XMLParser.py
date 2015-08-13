from bs4 import BeautifulSoup


class XMLParser(object):

    def __init__(self, filename=None):

        if(filename is None):
            self.parsedXML = BeautifulSoup(features='xml')
        else:
            self.parsedXML = BeautifulSoup(open(filename), "xml")

    def getTagAttr(self, tag, attr):
        return getattr(self.parsedXML, tag)[attr]

    def getChildTags(self, parent, child):
        return getattr(self.parsedXML, parent).find_all(child)

    def addTag(self, tagName, attrs):
        self.parsedXML.append(self.parsedXML.new_tag(tagName, **attrs))

    def appendToTag(self, tagParent, tagChild, attrs):
        getattr(self.parsedXML, tagParent).append(self.parsedXML.new_tag(tagChild, **attrs))

    def getXML(self):
        return self.parsedXML.prettify()

