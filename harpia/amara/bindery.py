__all__ = ['binder', 'TOP', 'ANY_NAMESPACE', 'REMOVE_RULE',
           'PY_REPLACE_PAT', 'RESERVED_NAMES']
import re
import sets
import keyword
import cStringIO
from xml import sax
from xml.dom import Node

from Ft.Xml.Domlette import NonvalidatingReader, XmlStrStrip
from Ft.Xml.Xslt import PatternList, OutputParameters, XmlWriter
from Ft.Xml import SplitQName

from harpia.amara import domtools
from harpia.amara import saxtools
#FIXME: Set up to use actual PyXML if available
from harpia.amara.pyxml_standins import *
from harpia.amara.binderyxpath import *


ANY_NAMESPACE = 'http://uche.ogbuji.net/amara/reserved/any-namespace'
TOP = -1
REMOVE_RULE = True

#FIXME: Use 4Suite L10N
def _(t): return t

g_namespaces = {}


class default_namer:
    '''
    Represents naming and conversion rules for Python and XML IDs
    '''
    def __init__(self):
        return

    def xml_to_python(self, qname, ns=None, check_clashes=None):
        prefix, local = SplitQName(qname)
        python_id = PY_REPLACE_PAT.sub('_', local)
        if python_id in RESERVED_NAMES:
            python_id = python_id + '_'
        if check_clashes:
            while python_id in check_clashes:
                python_id += '_'
        return python_id

    def python_to_xml(self, python_id):
        #XML NMTOKENS are a superset of Python IDs
        xml_name = python_id
        return xml_name


class namespace:
    def __init__(self, nsuri, common_prefix=None):
        self.nsuri = nsuri
        self.common_prefix = common_prefix
        self.binding_classes = {}
        return


class binder(saxtools.namespace_mixin, sax.ContentHandler,
             LexicalHandler, object):
    def __init__(self, prefixes=None):
        saxtools.namespace_mixin.__init__(self)
        self.prefixes = prefixes or {}
        self.binding = None
        self.binding_stack = []
        self.event = None
        #One list of rules for each DOM node type
        self.rules = {
            saxtools.START_ELEMENT: [default_element_rule().apply],
            saxtools.END_ELEMENT: [],
            saxtools.CHARACTER_DATA: [default_text_rule().apply],
            saxtools.PI: [default_pi_rule().apply],
            saxtools.COMMENT: [default_comment_rule().apply],
            saxtools.START_DOCUMENT: [default_root_rule().apply],
            saxtools.END_DOCUMENT: [],
            }
        #Keep track of the names at the level of the current element's
        #Children so correct positional predicates can be computed
        self.children = []
        #We have to keep a stack of the sibling names for
        #Each level so we don't lose context
        self.elem_name_stack = [[]]
        
        #Preferences
        self.preserve_comments = False
        self.state_machine = None
        self.xpatterns = []
        self.namer = default_namer()
        self.to_remove = self.event_type = None
        self.first_startelement = False
        return

    #Overridden ContentHandler methods
    def startDocument(self):
        if self.state_machine: self.state_machine.event(1, None, None)
        #Path components representing XPath steps to current element
        self.steps = [u'']
        self.event = (saxtools.START_DOCUMENT,)
        self.apply_rules()
        #self.binding_stack.append(self.apply_rules(saxtools.DOCUMENT_NODE))
        return

    def endDocument(self):
        if self.state_machine: self.state_machine.event(0, None, None)
        self.event = (saxtools.END_DOCUMENT,)
        self.apply_rules()
        return

    #Overridden DocumentHandler methods
    def startElementNS(self, name, qname, attribs):
        (ns, local) = name
        qname = self.name_to_qname(name)
        if self.state_machine: self.state_machine.event(1, ns, local)
        #Update list for sibling element names
        self.elem_name_stack[TOP].append(qname)
        #Count preceding siblings of the same name as current
        #(count starts at 1, as required by XPath, since we already
        #added the current name to the list)
        #name_count = len([ 1 for sib_name in self.elem_name_stack[TOP]
        #                  if sib_name == qname
        #                ])
        #Update steps list, using the computed positional predicate
        #self.steps.append(qname+'['+str(name_count)+']')
        #Stack things up properly for the child elements
        #self.elem_name_stack.append(self.children)
        #self.children = []
        self.event = (saxtools.START_ELEMENT, qname, ns, local, attribs)
        self.apply_rules()
        if not self.first_startelement:
            #Add prefixes discovered during parse of the top-level element
            #FIXME: What if the user does not want their manual mappings
            #Overriden by those in document?  (Probably a rare consideration)
            for prefix in self._prefix_ns:
                self.prefixes[prefix] = self._prefix_ns[prefix][0]
            self.first_startelement = True
        return

    def endElementNS(self, name, qname):
        (ns, local) = name
        qname = self.name_to_qname(name)
        if self.state_machine: self.state_machine.event(0, ns, local)
        #Pop back up the stack to level of siblings
        #self.elem_name_stack.pop()
        #self.steps.pop()
        self.event = (saxtools.END_ELEMENT, qname, ns, local)
        self.apply_rules()
        #self.binding_stack.pop()
        return

    def characters(self, text):
        #print u'/'.join(self.steps)
        self.event = (saxtools.CHARACTER_DATA, text)
        self.apply_rules()
        return

    def processingInstruction(self, target, data):
        self.event = (saxtools.PI, target, data)
        self.apply_rules()
        return

    #Overridden LexicalHandler methods
    def comment(self, body):
        #print "COMMENT", body
        self.event = (saxtools.COMMENT, body)
        self.apply_rules()
        return

    #def startDTD(self, name, public_id, system_id):
    #    print "START DTD", name, public_id, system_id
        return
        
    #Bindery methods
    def add_rule(self, rule, event_type=None):
        """
        Add a rule at a priority that depends on the target phase
        rule - the rule object
        You can also manipulate self.rules directly, but consider details
        such as add_rule hooks
        rule can be a function or an instance that defines an apply() function
        """
        target_phase = getattr(rule, 'target_phase', PRE_INSTANCE)
        if callable(rule):
            if target_phase == PRE_INSTANCE:
                self.rules[event_type].insert(0, rule)
            elif target_phase == POST_INSTANCE:
                self.rules[event_type].append(rule)
        else:
            if not event_type: event_type = rule.event_type
            if target_phase == PRE_INSTANCE:
                self.rules[event_type].insert(0, rule.apply)
            elif target_phase == POST_INSTANCE:
                self.rules[event_type].append(rule.apply)
            try:
                rule.add_rule_hook(self)
            except AttributeError:
                #No hook defined
                pass
        return

    def remove_rule(self, rule_callback, event_type):
        """
        Remove a rule for a given event.  Do so smartly.
        If we're within an apply_rules, don't screw up the loop
        rule - rule callback (function or "apply" method)
        """
        if event_type == self.event_type:
            self.to_remove.append(rule_callback)
        else:
            self.rules[event_type].remove(rule_callback)
        return

    def apply_rules(self):
        self.event_completely_handled = False
        self.event_type = self.event[0]
        self.to_remove = []
        #List copy is wasteful, but because of the dynamics of the mutation
        #within the loop, just about inevitable
        for rule_callback in self.rules[self.event_type][:]:
            rule_callback(self)
        for rc in self.to_remove:
            self.rules[self.event_type].remove(rc)
        self.to_remove = self.event_type = None
        return
        
    def set_binding_class(self, nsuri, local, class_):
        ns_class = g_namespaces.setdefault(nsuri, namespace(nsuri))
        ns_class.binding_classes[local] = class_
        return

    def read_xml(self, input_source):
        if self.xpatterns:
            self.state_machine = saxtools.xpattern_state_manager(
                self.xpatterns, self.prefixes)
        parser = sax.make_parser()
        normal_parser = saxtools.normalize_text_filter(parser)
        if self.preserve_comments:
            #Comments are the only thing we care about that requires
            #the special handler
            normal_parser.setProperty(
            #parser.setProperty(
                "http://xml.org/sax/properties/lexical-handler",
                self
                )
        normal_parser.setContentHandler(self)
        normal_parser.setFeature(sax.handler.feature_namespaces, 1)
        #parser.setContentHandler(self)
        #parser.setFeature(sax.handler.feature_namespaces, 1)
        normal_parser.parse(input_source)
        root = self.binding_stack[0]
        root.xmlns_prefixes = self.prefixes
        root.xml_namespaces = g_namespaces
        return root 


PY_REPLACE_PAT = re.compile(u'[^a-zA-Z0-9_]')

RESERVED_NAMES = [
    '__class__', '__delattr__', '__dict__', '__doc__', '__getattribute__',
    '__getitem__', '__hash__', '__init__', '__iter__', '__module__',
    '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    '__str__', '__unicode__', '__weakref__', '_childNodes', '_docIndex',
    '_localName', '_namespaceURI', '_parentNode', '_prefix', '_rootNode',
    'childNodes', 'docIndex', 
    'localName', 'namespaceURI', 'next_elem', 'nodeName', 'nodeType',
    'ownerDocument', 'parentNode', 'prefix', 'rootNode',
    ]

NO_NEED_TO_RESERVE = ['xml', 'xml_text_content', 'xml_xpath', 'xml_element',
                      'xml_clear', 'xml_parent', 'xml_attributes',
                      'xml_ignore_members', 'xml_doc']

RESERVED_NAMES += keyword.kwlist

RESERVED_NAMES = sets.ImmutableSet(RESERVED_NAMES)


#Phases to which rules should be added
#Usually there should only be one MAKE_INSTANCE phase rule, and this is
#Usually the default rule
#PRE_INSTANCE rules are usually for preventing certain events from creating objects
#POST_INSTANCE rules are usually for decorating or modifying created objects
PRE_INSTANCE, MAKE_INSTANCE, POST_INSTANCE = 1, 2, 3


def create_element(namer, qname, ns=None, ename=None):
    prefix, local = SplitQName(qname)
    if not ename: ename = namer.xml_to_python(qname, ns)
    ns_class = g_namespaces.setdefault(ns, namespace(ns, prefix))
    if ns_class.binding_classes.has_key(local):
        class_ = ns_class.binding_classes[local]
    else:
        exec "class %s(element_base): pass"%ename in globals(), locals()
        class_ = locals()[ename]
        ns_class.binding_classes[local] = class_
    instance = class_()
    instance.nodeName = qname
    if ns:
        #intern(ns) #Can't intern Unicode
        instance.xmlnsUri = ns
        instance.xmlnsPrefix = prefix
        instance.xmlnsLocalName = local
    instance.xml_namer = namer
    return instance


def bind_attributes(instance, parent, ename, binder):
    (dummy, qname, ns, local, attributes) = binder.event
    #Handle attributes by making them simple text data members
    #if attributes and not hasattr(instance, "xml_attributes"):
    if attributes:
        instance.xml_attributes = {}
    #No, "for aname in attributes" not possible because
    #AttributeListImpl diesn't play by those rules :-(
    for (ans, alocal), avalue in attributes.items():
        aqname = attributes.getQNameByName((ans, alocal))
        apyname = binder.namer.xml_to_python(aqname, ans,
                                             check_clashes=dir(instance))
        #setattr(instance, apyname, avalue)
        #Bypass __setattr__
        instance.__dict__[apyname] = avalue
        instance.xml_attributes[apyname] = (aqname, ans)
    return


def bind_instance(instance, parent):
    assert instance is not parent
    instance.xml_parent = parent
    parent.xml_children.append(instance)
    #Our test for element-ness.  is there a better one?
    if not hasattr(instance, "localName"):
        return instance
    #We now know that it's an element
    #qname = instance.nodeName
    local = instance.localName
    ns = instance.namespaceURI
    ename = parent.xml_namer.xml_to_python(local)
    instance.next_elem = None
    if hasattr(parent, ename):
        obj = getattr(parent, ename)
        if not hasattr(obj, "next_elem") or ns != obj.namespaceURI:
            ename = parent.xml_namer.xml_to_python(local, check_clashes=dir(parent))
            #Bypass __setattr__
            parent.__dict__[ename] = instance
        else:
            last = obj
            while last.next_elem:
                if last is last.next_elem:
                    raise BinderException(INSTANCE_ALREADY_BOUND)
                last = last.next_elem
            last.next_elem = instance
    else:
        #Bypass __setattr__
        parent.__dict__[ename] = instance
    instance.__dict__['next_elem'] = None
    return instance


class default_element_rule(object):
    def apply(self, binder):
        if binder.event_completely_handled:
            #Then another rule has already created an instance
            return
        parent = binder.binding_stack[TOP]
        if not parent: return
        
        (dummy, qname, ns, local, attributes) = binder.event
        prefix = qname[:qname.rindex(local)][:-1]
        ename = binder.namer.xml_to_python(local, ns, prefix)
        instance = create_element(binder.namer, qname, ns, ename)
        bind_attributes(instance, parent, ename, binder)
        instance = bind_instance(instance, parent)
        binder.binding_stack.append(instance)

        #Inset a trigger for handling the matching end element
        def handle_end(binder):
            if binder.event_completely_handled:
                return
            #if binder.binding_stack[-1] is instance:
            binder.binding_stack.pop()
            binder.event_completely_handled = True
            binder.remove_rule(handle_end, saxtools.END_ELEMENT)
            return
        handle_end.target_phase = POST_INSTANCE
        binder.add_rule(handle_end, saxtools.END_ELEMENT)
        return


class default_root_rule(object):
    def apply(self, binder):
        instance = root_base()
        instance.xml_namer = binder.namer
        binder.binding_stack.append(instance)
        return


class default_pi_rule(object):
    def apply(self, binder):
        if binder.event_completely_handled:
            #Then another rule has already created an instance
            return
        parent = binder.binding_stack[TOP]
        if not parent: return
        
        instance = pi_base()
        (dummy, target, data) = binder.event
        instance.target = target
        instance.data = data
        instance.xml_parent = parent
        parent.xml_children.append(instance)
        return


class default_comment_rule(object):
    def apply(self, binder):
        if binder.event_completely_handled:
            #Then another rule has already created an instance
            return
        parent = binder.binding_stack[TOP]
        if not parent: return
        
        instance = comment_base()
        (dummy, body) = binder.event
        instance.body = body
        instance.xml_parent = parent
        parent.xml_children.append(instance)
        return


class default_text_rule(object):
    def apply(self, binder):
        if binder.event_completely_handled:
            #Then another rule has already created an instance
            return
        parent = binder.binding_stack[TOP]
        if not parent: return
        
        (dummy, text) = binder.event
        parent.xml_children.append(text)
        #No actual binding object mapped to this node
        return


class default_container_node(object):
    #Mutation
    def xml_clear(self):
        "Remove all children"
        #Tempted to do
        #for i in len(self.xml_children): self.xml_remove_child(i)
        #But that would just be a pig
        self.xml_children = []
        for attr in self.__dict__:
            if not (attr in self.xml_ignore_members or attr.startswith('xml')):
                if getattr(self.__dict__[attr], 'next_elem', None):
                    #Does not unlink all the way down the next_elem chain,
                    #But GC should take care of them once the first is unlinked
                    del self.__dict__[attr]
        return

    def xml_append(self, obj):
        "Append element or text"
        if isinstance(obj, unicode):
            self.xml_children.append(obj)
        else:
            #Then it had better be an element object
            bind_instance(obj, self)
        return

    def xml_element(self, qname, ns=None, content=None, attributes=None):
        "Create a new, empty element (no attrs)"
        instance = create_element(self.xml_namer, qname, ns)
        if content:
            if not isinstance(content, list):
                content = [ content ]
            instance.xml_children = content
        if attributes:
            instance.xml_attributes = {}
            for aname in attributes:
                if isinstance(aname, tuple):
                    aqname, ans = aname
                else:
                    aqname, ans = aname, None
                avalue = attributes[aname]
                apyname = self.xml_namer.xml_to_python(
                    aqname, ans,
                    check_clashes=dir(instance))
                #Bypass __setattr__
                instance.__dict__[apyname] = avalue
                instance.xml_attributes[apyname] = (aqname, ans)
        return instance    

    def xml_remove_child(self, index=-1):
        "Remove child object"
        obj = self.xml_children[index]
        if isinstance(obj, unicode):
            del self.xml_children[index]
        else:
            #Remove references to the object
            #Probably a slow way to go about this
            for attr, val in self.__dict__.items():
                if not (attr.startswith('xml') or attr in self.xml_ignore_members):
                    next = getattr(val, 'next_elem', None)
                    if val == obj:
                        del self.__dict__[attr]
                        if next: self.__dict__[attr] = next
                    while next:
                        prev, val = val, next
                        next = getattr(val, 'next_elem', None)
                        if val == obj:
                            prev.next_elem = next
                            break
            del self.xml_children[index]
        return

    def xml_doc(self):
        msg = []
        xml_attrs = []
        if hasattr(self, 'xml_attributes'):
            msg.append('Object references based on XML attributes:')
            for apyname in self.xml_attributes:
                local, ns = self.xml_attributes[apyname]
                if ns:
                    source_phrase = " based on '{%s}%s' in XML"%(ns, local)
                else:
                    source_phrase = " based on '%s' in XML"%(local)
                msg.append(apyname+source_phrase)
                xml_attrs.append(apyname)
        msg.append('Object references based on XML child elements:')
        for attr, val in self.__dict__.items():
            if not (attr.startswith('xml') or attr in self.xml_ignore_members):
                if attr not in xml_attrs:
                    count = len(list(getattr(self, attr)))
                    if count == 1:
                        count_phrase = " (%s element)"%count
                    else:
                        count_phrase = " (%s elements)"%count
                    local, ns = val.localName, val.namespaceURI
                    if ns:
                        source_phrase = " based on '{%s}%s' in XML"%(ns, local)
                    else:
                        source_phrase = " based on '%s' in XML"%(local)
                    msg.append(attr+count_phrase+source_phrase)
        return u'\n'.join(msg)


class root_base(default_container_node, xpath_wrapper_mixin):
    """
    Base class for root nodes (similar to DOM documents
    and document fragments)
    """
    nodeType = Node.DOCUMENT_NODE
    xml_ignore_members = RESERVED_NAMES
    def __init__(self, namer=default_namer(), doctype_name=None, pubid=None,
                 sysid=None):
        self.xml_children = []
        self.nodeName = u'#document'
        self.xml_namer = namer
        if doctype_name:
            self.xml_pubid = pubid
            self.xml_sysid = sysid
            self.xml_doctype_name = doctype_name
        return

    def xml(self, stream=None, writer=None, **wargs):
        """
        serialize back to XML
        if stream is given, output to stream.  Function return value is None
        You can then set the following output parameters (among others):
            encoding - output encoding: default UTF-8
            omitXmlDeclaration - u'yes' to omit the XML decl (default u'no')
            cdataSectionElements - A list of element (namespace, local-name)
                                   And all matching elements are outptu as
                                   CDATA sections
            indent - u'yes' to pretty-print the XML (default u'no')
        other output parameters are supported, based on XSLT 1.0's xsl:output
        instruction, but use fo the others is encouraged only for very advanced
        users

        You can also just pass in your own writer instance, which might
        be useful if you want to output a SAX stream or DOM nodes

        If writer is given, use it directly (encoding can be set on the writer)
        if neither a stream nor a writer is given, return the output text
        as a Python string (not Unicode) encoded as UTF-8
        """
        temp_stream = None
        if not writer:
            #As a convenience, allow cdata section element defs to be simple QName
            if wargs.get('cdataSectionElements'):
                cdses = wargs['cdataSectionElements']
                cdses = [ isinstance(e, tuple) and e or (None, e)
                          for e in cdses ]
                wargs['cdataSectionElements'] = cdses
            if hasattr(self, "xml_sysid"):
                sysid, pubid = self.xml_sysid, self.xml_pubid
            else:
                sysid, pubid = None, None
            if stream:
                writer = create_writer(stream, wargs, pubid=pubid,
                                       sysid=sysid)
            else:
                temp_stream = cStringIO.StringIO()
                writer = create_writer(temp_stream, wargs,
                                       pubid=pubid,
                                       sysid=sysid)

        writer.startDocument()
        for child in self.xml_children:
            if isinstance(child, unicode):
                writer.text(child)
            else:
                child.xml(writer=writer)
        writer.endDocument()
        return temp_stream and temp_stream.getvalue()

    #Needed for Print and PrettyPrint
    #But should we support these, since we have xml(),
    #which can take a writer with indent="yes?"
    def _doctype(self):
        class doctype_wrapper(object):
            def __init__(self, name, pubid, sysid):
                self.name = name
                self.publicId = pubid
                self.systemId = sysid
                return
        if hasattr(self, "xml_sysid"):
            return doctype_wrapper(self.xml_doctype_name, self.xml_pubid,
                                   self.xml_sysid)
        else:
            return None

    doctype = property(_doctype)


class pi_base:
    nodeType = Node.PROCESSING_INSTRUCTION_NODE
    def __init__(self, target=None, data=None):
        self.target = target
        self.data = data
        return

    def xml(self, stream=None, writer=None):
        """
        If writer is None, stream cannot be None
        """
        if not writer: writer = create_writer(stream)
        writer.processingInstruction(self.target, self.data)
        return


class comment_base:
    nodeType = Node.COMMENT_NODE
    def __init__(self, body=None):
        self.body = body
        return

    def xml(self, stream=None, writer=None):
        """
        If writer is None, stream cannot be None
        """
        if not writer: writer = create_writer(stream)
        writer.comment(self.body)
        return


class element_iterator:
    def __init__(self, start):
        self.curr = start
        return

    def __iter__(self):
        return self

    def next(self):
        if not self.curr:
            raise StopIteration()
        result = self.curr
        if self.curr.next_elem:
            self.curr = self.curr.next_elem
        else:
            self.curr = None
        return result


class element_base(default_container_node, xpath_wrapper_mixin):
    nodeType = Node.ELEMENT_NODE
    #xml_ignore_members = ['nodeName']
    xml_ignore_members = RESERVED_NAMES
    def __init__(self, namer=default_namer()):
        self.xml_children = []
        self.next_elem = None
        self.xml_namer = namer
        return

    def __iter__(self):
        return element_iterator(self)

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self)[key]
        else:
            #if isinstance(key, tuple) and len(key) == 2:
            if isinstance(key, basestring):
                key = (key, None)
            for pyname in self.xml_attributes:
                if self.xml_attributes[pyname] == key:
                    result = getattr(self, pyname)
            else:
                raise KeyError('Inappropriate key (%s)'%(key))
            return 

    def __setitem__(self, key, value):
        if isinstance(key, int):
            child = self.__getitem__(key)
            child.xml_clear()
            child.xml_children = [value]
        else:
            #if isinstance(key, tuple) and len(key) == 2:
            if isinstance(key, basestring):
                key = (key, None)
            for pyname in self.xml_attributes:
                if self.xml_attributes[pyname] == key:
                    #setattr(self, pyname, value)
                    #Bypass __setattr__
                    self.__dict__[pyname] = value
            else:
                raise KeyError('Inappropriate key (%s)'%(str(key)))
        return 

    def __delitem__(self, key):
        if isinstance(key, int):
            child = self.__getitem__(key)
            index = self.xml_parent.xml_children.index(child)
            self.xml_parent.xml_remove_child(index)
        return 

    def __delattr__(self, key):
        if key.startswith('xml') or key in RESERVED_NAMES:
            del self.__dict__[key]
            return
        ref = getattr(self, key)
        #Our test for element-ness.  is there a better one?
        if hasattr(ref, "localName"):
            ref.__delitem__(0)
        elif isinstance(ref, unicode):
            del self.__dict__[key]
            del self.xml_attributes[key]
        return

    def __setattr__(self, key, value):
        if key.startswith('xml') or key in RESERVED_NAMES:
            self.__dict__[key] = value
            return
        if hasattr(self, key):
            ref = getattr(self, key)
            #Our test for element-ness.  is there a better one?
            if hasattr(ref, "localName"):
                ref.xml_clear()
                ref.xml_children = [value]
            elif isinstance(ref, unicode):
                self.__dict__[key] = value
            return
        elif isinstance(value, unicode):
            self.__dict__[key] = value
            if not hasattr(self, 'xml_attributes'):
                self.xml_attributes = {}
            self.xml_attributes[key] = (key, None)
        else:
            raise ValueError('Inappropriate set attribute request: key (%s), value (%s)'%(key, value))
        return

    def xml_set_attribute(self, aname, avalue):
        "Set (or create) an attribute on ana element"
        if isinstance(aname, tuple):
            aqname, ans = aname
        else:
            aqname, ans = aname, None
        apyname = self.xml_namer.xml_to_python(
            aqname, ans,
            check_clashes=dir(self))
        #Bypass __setattr__
        self.__dict__[apyname] = avalue
        if not hasattr(self, 'xml_attributes'):
            self.xml_attributes = {}
        self.xml_attributes[apyname] = (aqname, ans)
        return apyname

    #def __setattr__(self, attr, value):
        #Equivalent to creating a bound attribute
    #    self.__dict__[attr] = value
    #    return

    #def count(self):
    #    return len(list(self))

    def xml_text_content(self):
        return u''.join([ ch for ch in self.xml_children
                            if isinstance(ch, unicode)])

    __unicode__ = xml_text_content

    def __str__(self):
        return str(self.xml_text_content())

    def xml(self, stream=None, writer=None, **wargs):
        """
        serialize back to XML
        if stream is given, output to stream.  Function return value is None
        You can then set the following output parameters (among others):
            encoding - output encoding: default u'UTF-8'
            omitXmlDeclaration - u'no' to include an XML decl (default u'yes')
            cdataSectionElements - A list of element (namespace, local-name)
                                   And all matching elements are outptu as
                                   CDATA sections
            indent - u'yes' to pretty-print the XML (default u'no')
        other output parameters are supported, based on XSLT 1.0's xsl:output
        instruction, but use fo the others is encouraged only for very advanced
        users

        You can also just pass in your own writer instance, which might
        be useful if you want to output a SAX stream or DOM nodes

        If writer is given, use it directly (encoding can be set on the writer)
        if neither a stream nor a writer is given, return the output text
        as a Python string (not Unicode) encoded as UTF-8
        """
        temp_stream = None
        close_document = 0
        if not writer:
            #Change the default to *not* generating an XML decl
            if not wargs.get('omitXmlDeclaration'):
                wargs['omitXmlDeclaration'] = u'yes'
            if stream:
                writer = create_writer(stream, wargs)
            else:
                temp_stream = cStringIO.StringIO()
                writer = create_writer(temp_stream, wargs)

            writer.startDocument()
            close_document = 1
        writer.startElement(self.nodeName, self.namespaceURI)
        if hasattr(self, 'xml_attributes'):
            for apyname in self.xml_attributes:
                aqname, ans = self.xml_attributes[apyname]
                val = self.__dict__[apyname]
                writer.attribute(aqname, val, ans)
        for child in self.xml_children:
            if isinstance(child, unicode):
                writer.text(child)
            else:
                child.xml(writer=writer)
        writer.endElement(self.nodeName, self.namespaceURI)
        if close_document:
            writer.endDocument()
        return temp_stream and temp_stream.getvalue()
    
    def xml_index_on_parent(self):
        try:
            index = self.xml_parent.xml_children.index(self)
        except ValueError: #Not found
            raise
        return index


def create_writer(stream, wargs=None, pubid=None, sysid=None, encoding="UTF-8"):
    wargs = wargs or {}
    if not stream:
        raise BinderException(NO_STREAM_GIVEN_FOR_UNBIND)
    op = OutputParameters.OutputParameters()
    for arg in wargs:
        setattr(op, arg, wargs[arg])
    #Doctype info in the document object override any given explicitly
    if sysid: op.doctypeSystem = sysid
    if pubid: op.doctypePublic = pubid
    #writer = XmlWriter.XmlWriter(op, stream)
    writer = XmlWriter.CdataSectionXmlWriter(op, stream)
    return writer


class BinderException(Exception):
    pass


#CLASH_BETWEEN_SCALAR_AND_SUBELEM = _('Bindery does not yet handle a name clash between an attribute and a child element')
NO_STREAM_GIVEN_FOR_UNBIND = _('You must provide a stream for the output of the xml method (serialization)')
INSTANCE_ALREADY_BOUND = _('Instance already bound to parent')

