from xml.dom import Node
from xml.dom import EMPTY_NAMESPACE as NULL_NAMESPACE
from xml.dom import EMPTY_PREFIX as NULL_PREFIX

from Ft.Xml.XPath.Context import Context
from Ft.Xml.XPath import Evaluate
from Ft.Xml import SplitQName

#FIXME: Use 4Suite L10N
def _(t): return t


class dummy_node_wrapper(object):
    def _docIndex(self):
        return 0

    docIndex = property(_docIndex)

    def _xpathAttributes(self):
        return []

    xpathAttributes = property(_xpathAttributes)

    def _childNodes(self):
        return []

    childNodes = property(_childNodes)

    def __cmp__(self, other):
        return cmp(self.docIndex, other.docIndex)


class xpath_attr_wrapper(dummy_node_wrapper):
    nodeType = Node.ATTRIBUTE_NODE
    def __init__(self, qname, ns, value, parent):
        self.namespaceURI = ns
        self.prefix, self.localName = SplitQName(qname)
        self.value = value
        self.nodeValue = value
        self.name = qname
        self.nodeName = qname
        self.rootNode = parent._rootNode()
        docIndex = id(value)
        return

    def __unicode__(self):
        return self.value


class text_wrapper(dummy_node_wrapper):
    nodeType = Node.TEXT_NODE
    def __init__(self, st, parent):
        self.data = st
        self.parentNode = parent
        docIndex = id(st)
        return

    def __unicode__(self):
        return self.data

    def _rootNode(self):
        return self.parentNode._rootNode()

    rootNode = property(_rootNode)
    ownerDocument = rootNode

    def _docIndex(self):
        #print "text_wrapper._docIndex"
        return 1

    docIndex = property(_docIndex)


class xpath_wrapper_mixin(object):
    def xml_xpath(self, query):
        """
        Execute an XPath query with this object standing in for the
        context node.  The namespace mappings are taken from the root
        binding object.  There are no variable bindings.  Most XPath
        is supported.
        query - a unicode object expressing an XPath
        The return value depends on the XPath expression (expr)
        - If expr reults in an XPath string, the return value is a
        Python Unicode object
        - If expr reults in an XPath number, the return value is a
        Python float
        - If expr reults in an XPath boolean, the return value is a
        Python bool object
        - If expr reults in an XPath node set, the return value is a
        Python list (always a list, even if empty, or a node with just
        one entry)
        """
        ctx = Context(self, processorNss=self.rootNode.xmlns_prefixes)
        result = Evaluate(query, context=ctx)
        return result

    def _namespaceURI(self):
        try:
            return self.xmlnsUri
        except AttributeError:
            return NULL_NAMESPACE

    namespaceURI = property(_namespaceURI)

    def _localName(self):
        try:
            return self.xmlnsLocalName
        except AttributeError:
            lname = self.nodeName
            if lname[0] == '#': lname = None
            return lname

    localName = property(_localName)

    def _prefix(self):
        try:
            return self.xmlnsPrefix
        except AttributeError:
            return NULL_PREFIX

    prefix = property(_prefix)

    def _parentNode(self):
        try:
            return self.xml_parent
        except AttributeError:
            return None

    parentNode = property(_parentNode)

    def _rootNode(self):
        if self.parentNode:
            return self.parentNode._rootNode()
        return self

    rootNode = property(_rootNode)
    ownerDocument = rootNode

    def _childNodes(self):
        children = []
        for node in self.xml_children:
            if hasattr(node, 'next_elem'):
                children.append(node)
            elif isinstance(node, unicode):
                children.append(text_wrapper(node, self))
        return children

    childNodes = property(_childNodes)

    def _xpathAttributes(self):
        try:
            attrs = self.xml_attributes
        except AttributeError:
            return []
        return [ xpath_attr_wrapper(qname, ns, unicode(getattr(self, attr)), self)
                 for attr, (qname, ns) in self.xml_attributes.items() ]

    xpathAttributes = property(_xpathAttributes)

    def _attributes(self):
        try:
            attrs = self.xml_attributes
        except AttributeError:
            return {}
        keys = [ (ns, SplitQName(qname)) 
                   for attr, (qname, ns) in self.xml_attributes.items() ]
        values = [ xpath_attr_wrapper(qname, ns, unicode(getattr(self, attr)), self)
                   for attr, (qname, ns) in self.xml_attributes.items() ]
        return dict(zip(keys, values))

    attributes = property(_attributes)

    def getAttributeNS(self, ns, local):
        try:
            attrs = self.xml_attributes
        except AttributeError:
            return {}
        keys = [ (ns, SplitQName(qname)[1]) 
                   for attr, (qname, ns) in self.xml_attributes.items() ]
        values = [ unicode(getattr(self, attr))
                   for attr, (qname, ns) in self.xml_attributes.items() ]
        attr_dict = dict(zip(keys, values))
        return attr_dict.get((ns, local), "")

    def _docIndex(self):
        #print "_docIndex", self.nodeType
        return id(self)

    docIndex = property(_docIndex)

    def __cmp__(self, other):
        try:
            return cmp(self.docIndex, other.docIndex)
        except AttributeError:
            return -cmp(other, unicode(self))


class BinderXpathException(Exception):
    pass

NO_ATTRIBUTE_SUPPORT = _('You have attempted to use an XPath expression that requires attribute support in the binding.  Try using the rule amara.binderytools.preserve_attribute_details.')

