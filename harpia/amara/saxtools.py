#Python 2.3 or higher required
from xml import sax
from xml.dom import EMPTY_NAMESPACE as NULL_NAMESPACE
from xml.dom import EMPTY_PREFIX as NULL_PREFIX
from xml.dom import XML_NAMESPACE
from xml.dom import Node
from Ft.Xml import Domlette

START_DOCUMENT               = 1
END_DOCUMENT                 = 2
START_ELEMENT                = 3
END_ELEMENT                  = 4
CHARACTER_DATA               = 10
COMMENT                      = 11
PI                           = 12

#
# namespace_mixin is a utility that helps manage namespace prefix mappings
#

class namespace_mixin:
    def __init__(self):
        self._ns_prefix = {XML_NAMESPACE: [u'xml'], NULL_NAMESPACE: [NULL_PREFIX]}
        self._prefix_ns = {u'xml': [XML_NAMESPACE], NULL_PREFIX: [NULL_NAMESPACE]}
        return
    
    def startPrefixMapping(self, prefix, uri):
        self._ns_prefix.setdefault(uri, []).append(prefix)
        self._prefix_ns.setdefault(prefix, []).append(uri)
        return

    def endPrefixMapping(self, prefix):
        uri = self._prefix_ns[prefix].pop()
        prefix = self._ns_prefix[uri].pop()
        #assert prefix == uri
        return

    def name_to_qname(self, name):
        #print self._ns_prefix
        #print self._prefix_ns
        uri, local = name
        prefix = self._ns_prefix[uri][-1]
        qname = ( prefix and ( prefix + u':' ) or '') + local
        return qname


#
# Tenorsax framework: helps linerarize SAX logic
#

class tenorsax(namespace_mixin, sax.ContentHandler):
    def __init__(self, consumer):
        namespace_mixin.__init__(self)
        self.consumer = consumer
        self.dispatcher = consumer.top_dispatcher
        self.curr_gen = None
        return
    
    def startElementNS(self, name, qname, attributes):
        (ns, local) = name
        qname = self.name_to_qname(name)
        #print "Start element", (name, qname)
        self.consumer.event = (START_ELEMENT, ns, local)
        self.consumer.params = attributes
        self.curr_gen = tenorsax.event_loop_body(self.dispatcher, self.curr_gen, self.consumer.event)
        return
    
    def endElementNS(self, name, qname):
        (ns, local) = name
        qname = self.name_to_qname(name)
        #print "end element", (name, qname)
        self.consumer.event = (END_ELEMENT, ns, local)
        self.consumer.params = None
        self.curr_gen = tenorsax.event_loop_body(self.dispatcher, self.curr_gen, self.consumer.event)
        return
    
    def characters(self, text):
        #print "characters", text
        self.consumer.event = (CHARACTER_DATA,)
        self.consumer.params = text
        self.curr_gen = tenorsax.event_loop_body(self.dispatcher, self.curr_gen, self.consumer.event)
        return

    def event_loop_body(dispatcher, curr_gen, event):
        if curr_gen:
            curr_gen = tenorsax.execute_delegate(curr_gen)
        else:
            curr_gen = tenorsax.check_for_delegate(dispatcher, event)
        return curr_gen
    event_loop_body = staticmethod(event_loop_body)

    def execute_delegate(curr_gen):
        try:
            curr_gen.next()
        except StopIteration:
            curr_gen = None
        return curr_gen
    execute_delegate = staticmethod(execute_delegate)

    def check_for_delegate(dispatcher, event):
        if event[0] == START_ELEMENT:
            end_condition = (END_ELEMENT,) + event[1:]
        else:
            end_condition = None
        curr_gen = None
        delegate_generator = dispatcher.get(event)
        if delegate_generator:
            #Fire up the generator
            curr_gen = delegate_generator(end_condition)
            try:
                curr_gen.next()
            except StopIteration:
                print "immediate end"
                #Immediate generator termination
                curr_gen = None
        return curr_gen
    check_for_delegate = staticmethod(check_for_delegate)

#
#
#

from xml import sax
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE
from xml.dom import EMPTY_NAMESPACE as NULL_NAMESPACE
from xml.dom import EMPTY_PREFIX as NULL_PREFIX

from Ft.Xml.Xslt import parser as XPatternParser

from Ft.Xml.Xslt.XPatterns import Patterns
from Ft.Xml.Xslt.XPatterns import Pattern
from Ft.Xml.Xslt.XPatterns import DocumentNodeTest
from Ft.Xml.XPath.ParsedNodeTest import LocalNameTest
from Ft.Xml.XPath.ParsedNodeTest import NamespaceTest
from Ft.Xml.XPath.ParsedNodeTest import QualifiedNameTest
from Ft.Xml.XPath.ParsedNodeTest import PrincipalTypeTest

DUMMY_DOCELEM = u'dummy'
START_STATE = 0
TOP = -1
ANY = '?'
#Used to figure out whether a wildcard event is user-specified,
#Or added internally
EXPLICIT, IMPLICIT = (True, False)


class xpattern_state_machine:
    """
    A simple state machine that interprets XPatterns
    A state is "live" when it represents the successful completion
    of an XPattern.
    """
    PARSER = XPatternParser.new()
    
    def __init__(self, repr_xp, xp, nss):
        self._state_table = {START_STATE: {}}
        self._live_states = {}
        self._ignored_subtree_states = []
        self._substate_depth = 0
        newest_state = START_STATE
        last_state = START_STATE
        for subpat in xp.patterns:
            steps = subpat.steps[:]
            steps.reverse()
            for (step_count, (axis_type, node_test, ancestor)) in enumerate(steps):
                if isinstance(node_test, DocumentNodeTest):
                    start_event = (1, None, None)
                    end_event = (0, None, None)
                elif isinstance(node_test, LocalNameTest):
                    if node_test.nodeType == Node.ELEMENT_NODE:
                        start_event = (1, None, node_test._name)
                        end_event = (0, None, node_test._name)
                    else:
                        continue
                elif isinstance(node_test, QualifiedNameTest):
                    if node_test.nodeType == Node.ELEMENT_NODE:
                        ns = nss[node_test._prefix]
                        start_event = (1, ns, node_test._localName)
                        end_event = (0, ns, node_test._localName)
                    else:
                        continue
                elif isinstance(node_test, PrincipalTypeTest):
                    if node_test.nodeType == Node.ELEMENT_NODE:
                        start_event = (1, ANY, EXPLICIT)
                        end_event = (0, ANY, EXPLICIT)
                    else:
                        continue
                elif isinstance(node_test, NamespaceTest):
                    if node_test.nodeType == Node.ELEMENT_NODE:
                        ns = nss[node_test._prefix]
                        start_event = (1, ns, ANY)
                        end_event = (0, ns, ANY)
                    else:
                        continue
                else:
                    import sys; print >> sys.stderr, "Pattern step not supported:", (axis_type, node_test, ancestor), "Node test class", node_test.__class__
                    continue

                if self._state_table[last_state].has_key(start_event):
                    top_state = self._state_table[last_state][start_event]
                else:
                    newest_state += 1
                    top_state = newest_state
                    self._state_table[top_state] = {}
                self._state_table[last_state][start_event] = top_state
                self._state_table[top_state][end_event] = last_state
                last_state = top_state
                complete_state = top_state #The state representing completion of an XPattern
                if step_count and not ancestor:
                    #Insert a state, which handles any child element
                    #Not explicitly matching some other state (so that
                    #/a/b/c is not a mistaken match for XPattern /a/c)
                    start_event = (1, ANY, IMPLICIT)
                    end_event = (0, ANY, IMPLICIT)
                    newest_state += 1
                    self._state_table[newest_state] = {}
                    self._state_table[parent_start_element_event][start_event] = newest_state
                    self._state_table[newest_state][end_event] = parent_start_element_event
                    self._ignored_subtree_states.append(newest_state)
                parent_start_element_event = top_state
            self._live_states[top_state] = repr_xp
        #print self._state_table
        #print self._live_states
        self._state = START_STATE
        self.entering_xpatterns = []
        self.leaving_xpatterns = []
        self.current_xpatterns = []
        self.tree_depth = 0
        self.depth_marks = []
        return

    def event(self, is_start, ns, local):
        """
        Register an event and effect ant state transitions
        found in the state table
        """
        #We only have a chunk ready for the handler in
        #the explicit case below
        self.entering_xpatterns = []
        self.leaving_xpatterns = []
        self.tree_depth += is_start and 1 or -1
        #print "event", (is_start, ns, local), self._state, self.tree_depth, self.depth_marks
        #An end event is never significant unless we know we're expecting it
        if not is_start and self.depth_marks and self.tree_depth != self.depth_marks[-1]:
            return self._state
        lookup_from = self._state_table[self._state]
        #FIXME: second part should be an element node test "*", should not match, say, start document
        if not lookup_from.has_key((is_start, ns, local)) and (ns, local) == (None, None):
            return self._state

        if lookup_from.has_key((is_start, ns, local)) or lookup_from.has_key((is_start, ns, ANY)):
            try:
                new_state = lookup_from[(is_start, ns, local)]
            except KeyError:
                new_state = lookup_from[(is_start, ns, ANY)]
            if (new_state in self._live_states):
                #Entering a defined XPattern chunk
                self.entering_xpatterns.append(self._live_states[new_state])
                self.current_xpatterns.append(self._live_states[new_state])
            elif (self._state in self._live_states):
                #Leaving a defined XPattern chunk
                self.leaving_xpatterns.append(self.current_xpatterns.pop())
            if is_start:
                self.depth_marks.append(self.tree_depth - 1)
            else:
                self.depth_marks.pop()
            self._state = new_state
        elif lookup_from.has_key((is_start, ANY, EXPLICIT)):
            new_state = lookup_from[(is_start, ANY, EXPLICIT)]
            if (new_state in self._live_states):
                #Entering a defined XPattern chunk
                self.entering_xpatterns.append(self._live_states[new_state])
                self.current_xpatterns.append(self._live_states[new_state])
            elif (self._state in self._live_states):
                #Leaving a defined XPattern chunk
                self.leaving_xpatterns.append(self.current_xpatterns.pop())
            self._state = new_state
            if is_start:
                self.depth_marks.append(self.tree_depth - 1)
            else:
                self.depth_marks.pop()
        elif lookup_from.has_key((is_start, ANY, IMPLICIT)):
            new_state = lookup_from[(is_start, ANY, IMPLICIT)]
            self._state = new_state
            if is_start:
                self.depth_marks.append(self.tree_depth - 1)
            else:
                self.depth_marks.pop()
        #print self.entering_xpatterns,self.leaving_xpatterns,self.current_xpatterns
        return self._state

    def status(self):
        """
        1 if currently within an XPattern, 0 if not
        Calling code might also want to just check
        self.current_xpatterns directly
        """
        return not not self.current_xpatterns


class xpattern_state_manager:
    """
    And aggregation of multiple state machines, one for each registered pattern
    """
    PARSER = XPatternParser.new()
    
    def __init__(self, xpatterns, nss):
        if not hasattr(xpatterns[0], "match"):
            self._xpatterns = [ (p, self.PARSER.parse(p)) for p in xpatterns ]
        else:
            self._xpatterns = [ (repr(xp), self.PARSER.parse(p)) for p in xpatterns ]
        self._machines = [ xpattern_state_machine(repr_xp, xp, nss) for repr_xp, xp in self._xpatterns ]
        return

    def event(self, is_start, ns, local):
        for machine in self._machines:
            machine.event(is_start, ns, local)
        #FIXME: Slow and clumsy
        self.entering_xpatterns = []
        self.leaving_xpatterns = []
        self.current_xpatterns = []
        for m in self._machines:
            self.entering_xpatterns.extend(m.entering_xpatterns)
            self.leaving_xpatterns.extend(m.leaving_xpatterns)
            self.current_xpatterns.extend(m.current_xpatterns)
        #print "manager event", (self.entering_xpatterns, self.leaving_xpatterns, self.current_xpatterns)
        return

    def status(self):
        """
        1 if currently within an XPattern, 0 if not
        Calling code might also want to just check
        self.current_xpatterns directly
        """
        return not not self.current_xpatterns


class sax2dom_chunker(namespace_mixin, sax.ContentHandler):
    """
    Note: Ignores nodes prior to the document element, such as PIs and
    text nodes.  Collapses CDATA sections into plain text
    Only designed to work if you set the feature
      sax.handler.feature_namespaces
    to 1 on the parser you use.

    xpatterns - list of XPatterns.  Only portions of the
        tree within these patterns will be instantiated as DOM (as
        chunks fed to chunk_consumer in sequence)
        If None (the default, a DOM node will be created representing
        the entire tree.

    nss - a dictionary of prefix -> namespace name mappings used to
        interpret XPatterns
    
    chunk_consumer - a callable object taking a DOM node.  It will be
        invoked as each DOM chunk is prepared.
    
    domimpl - DOM implemention to build, e.g. mindom (the default)
        or cDomlette or pxdom (if you have the right third-party
        packages installed).
    
    owner_doc - for advanced uses, if you want to use an existing
        DOM document object as the owner of all created nodes.
        
    """
    def __init__(self,
                 xpatterns=None,
                 nss=None,
                 chunk_consumer=None,
                 domimpl=Domlette.implementation,
                 owner_doc=None,
                 ):
        namespace_mixin.__init__(self)
        nss = nss or {}
        #HINT: To use minidom
        #domimpl = xml.dom.minidom.getDOMImplementation()
        self._impl = domimpl
        if isinstance(xpatterns, str) or isinstance(xpatterns, unicode) :
            xpatterns = [xpatterns]
        #print xpatterns
        if owner_doc:
            self._owner_doc = owner_doc
        else:
            try:
                dt = self._impl.createDocumentType(DUMMY_DOCELEM, None, u'')
            except AttributeError:
                #Domlette doesn't need createDocumentType
                dt = None
            self._owner_doc = self._impl.createDocument(
                DUMMY_DOCELEM, DUMMY_DOCELEM, dt)
        #Create a docfrag to hold all the generated nodes.
        root_node = self._owner_doc.createDocumentFragment()
        self._nodeStack = [ root_node ]
        self.state_machine = xpattern_state_manager(xpatterns, nss)
        self._chunk_consumer = chunk_consumer
        return

    def get_root_node(self):
        """
        Only useful if the user does not register trim paths
        If so, then after SAX processing the user can call this
        method to retrieve resulting DOM representing the entire
        document
        """
        return self._nodeStack[0]

    #Overridden ContentHandler methods
    def startDocument(self):
        self.state_machine.event(1, None, None)
        return

    def endDocument(self):
        self.state_machine.event(0, None, None)
        return

    def startElementNS(self, name, qname, attribs):
        (ns, local) = name
        qname = self.name_to_qname(name)
        self.state_machine.event(1, ns, local)
        if not self.state_machine.status():
            return
        new_element = self._owner_doc.createElementNS(ns, qname or local)

        #No, "for aname in attributes" not possible because
        #AttributeListImpl diesn't play by those rules :-(
        for ((attr_ns, lname), value) in attribs.items():
            if attr_ns is not None:
                attr_qname = attribs.getQNameByName((attr_ns, lname))
            else:
                attr_qname = lname
            attr = self._owner_doc.createAttributeNS(
                attr_ns, attr_qname)
            attr_qname = attribs.getQNameByName((attr_ns, lname))
            attr.value = value
            new_element.setAttributeNodeNS(attr)

        self._nodeStack.append(new_element)
        return

    def endElementNS(self, name, qname):
        (ns, local) = name
        qname = self.name_to_qname(name)
        self.state_machine.event(0, ns, local)
        if not self.state_machine.status():
            if (self._chunk_consumer and
                self.state_machine.leaving_xpatterns):
                #Complete the element being closed because it
                #Is the last bit of a DOM to be fed to the consumer
                new_element = self._nodeStack[TOP]
                del self._nodeStack[TOP]
                self._nodeStack[TOP].appendChild(new_element)
                #Feed the consumer
                self._chunk_consumer(self._nodeStack[0])
                #Start all over with a new doc frag so the old
                #One's memory can be reclaimed
                root_node = self._owner_doc.createDocumentFragment()
                self._nodeStack = [ root_node ]
            return
        new_element = self._nodeStack[TOP]
        del self._nodeStack[TOP]
        self._nodeStack[TOP].appendChild(new_element)
        return

    def processingInstruction(self, target, data):
        if self.state_machine.status():
            pi = self._owner_doc.createProcessingInstruction(
                target, data)
            self._nodeStack[TOP].appendChild(pi)
        return

    def characters(self, chars):
        if self.state_machine.status():
            new_text = self._owner_doc.createTextNode(chars)
            self._nodeStack[TOP].appendChild(new_text)
        return

    #Overridden LexicalHandler methods
    def comment(self, text):
        if self.state_machine.status():
            new_comment = self._owner_doc.createComment(text)
            self._nodeStack[TOP].appendChild(new_comment)
        return


from xml.sax.saxutils import XMLFilterBase
#FIXME: Set up to use actual PyXML if available
from harpia.amara.pyxml_standins import *

class normalize_text_filter(XMLFilterBase, LexicalHandler):
    """
    SAX filter to ensure that contiguous white space nodes are
    delivered merged into a single node
    """
    def __init__(self, *args):
        XMLFilterBase.__init__(self, *args)
        self._accumulator = []
        return

    def _complete_text_node(self):
        if self._accumulator:
            XMLFilterBase.characters(self, ''.join(self._accumulator))
            self._accumulator = []
        return

    def startDocument(self):
        XMLFilterBase.startDocument(self)
        return

    def endDocument(self):
        XMLFilterBase.endDocument(self)
        return

    def startElement(self, name, attrs):
        self._complete_text_node()
        XMLFilterBase.startElement(self, name, attrs)
        return

    def startElementNS(self, name, qname, attrs):
        self._complete_text_node()
        #A bug in Python 2.3 means that we can't just defer to parent, which is broken
        #XMLFilterBase.startElementNS(self, name, qname, attrs)
        self._cont_handler.startElementNS(name, qname, attrs)
        return

    def endElement(self, name):
        self._complete_text_node()
        XMLFilterBase.endElement(self, name)
        return

    def endElementNS(self, name, qname):
        self._complete_text_node()
        XMLFilterBase.endElementNS(self, name, qname)
        return

    def processingInstruction(self, target, body):
        self._complete_text_node()
        XMLFilterBase.processingInstruction(self, target, body)
        return

    def comment(self, body):
        self._complete_text_node()
        #No such thing as an XMLFilterBase.comment :-(
        #XMLFilterBase.comment(self, body)
        self._cont_handler.comment(body)
        return

    def characters(self, text):
        self._accumulator.append(text)
        return

    def ignorableWhitespace(self, ws):
        self._accumulator.append(text)
        return

    #Must be overridden because of a bug in Python 2.0 through 2.4
    #And even still in PyXML 0.8.4.  Missing "return"
    def resolveEntity(self, publicId, systemId):
        return self._ent_handler.resolveEntity(publicId, systemId)

    # Enhancement suggested by James Kew:
    # Override XMLFilterBase.parse to connect the LexicalHandler
    # Can only do this by setting the relevant property
    # May throw SAXNotSupportedException
    def parse(self, source):
        #import inspect; import pprint; pprint.pprint(inspect.stack())
        self._parent.setProperty(property_lexical_handler, self)
        # Delegate to XMLFilterBase for the rest
        XMLFilterBase.parse(self, source)
        return


#
# From xml.dom
#

#ELEMENT_NODE                = 1
#ATTRIBUTE_NODE              = 2
#TEXT_NODE                   = 3
#CDATA_SECTION_NODE          = 4
#ENTITY_REFERENCE_NODE       = 5
#ENTITY_NODE                 = 6
#PROCESSING_INSTRUCTION_NODE = 7
#COMMENT_NODE                = 8
#DOCUMENT_NODE               = 9
#DOCUMENT_TYPE_NODE          = 10
#DOCUMENT_FRAGMENT_NODE      = 11
#NOTATION_NODE               = 12

