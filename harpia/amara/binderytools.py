"""
Convenience functions for using the Amara bindery.
"""

#
# Utility functions for common binding usage
#

import re
import time
from datetime import time as dt_time
from datetime import datetime, timedelta
from Ft.Xml import InputSource
from Ft.Xml import SplitQName
from Ft.Lib import Uri
from harpia.amara import bindery
from harpia.amara import domtools
from harpia.amara import saxtools

#FIXME: Use 4Suite L10N
def _(t): return t


#Regexen from Mark Nottingham (http://www.mnot.net/python/isodate.py)
DATETIME_PAT = re.compile(r"""
    (?P<year>\d{4,4})
    (?:
        -
        (?P<month>\d{1,2})
        (?:
            -
            (?P<day>\d{1,2})
            (?:
                T
                (?P<hour>\d{1,2})
                :
                (?P<minute>\d{1,2})
                (?:
                    :
                    (?P<second>\d{1,2})
                    (?:
                        \.
                        (?P<fract_second>\d+)?
                    )?
                )?                    
                (?:
                    Z
                    |
                    (?:
                        (?P<tz_sign>[+-])
                        (?P<tz_hour>\d{1,2})
                        :
                        (?P<tz_min>\d{2,2})
                    )
                )
            )?
        )?
    )?
$""", re.VERBOSE)


TIME_PAT = re.compile(r"""
                (?P<hour>\d{1,2})
                :
                (?P<minute>\d{1,2})
                (?:
                    :
                    (?P<second>\d{1,2})
                    (?:
                        \.
                        (?P<fract_second>\d+)?
                    )?
                )?                    
                (?:
                    Z
                    |
                    (?:
                        (?P<tz_sign>[+-])
                        (?P<tz_hour>\d{1,2})
                        :
                        (?P<tz_min>\d{2,2})
                    )
                )
$""", re.VERBOSE)


def parse_isodate(st):
    """
    st - string or Unicode with ISO 8601 date
    """
    m = DATETIME_PAT.match(st)
    if not m:
        return None
    gd = m.groupdict('0')
    #FIXME: does not handle time zones except for UTC (trailing "Z")
    dt = datetime(int(gd['year']), 
                  int(gd['month']) or 1, 
                  int(gd['day']) or 1, 
                  int(gd['hour']), 
                  int(gd['minute']),
                  int(gd['second']),
                  int(float(u'.' + gd['fract_second'])*1000000),
                  )
    if st[-1] == 'Z':
        zone = time.daylight and time.altzone or time.timezone
        dt -= timedelta(0, zone)
    return dt


def parse_isotime(st):
    """
    st - string or Unicode with ISO 8601 time
    """
    m = TIME_PAT.match(st)
    if not m:
        return None
    gd = m.groupdict('0')
    #FIXME: does not handle time zones
    t = dt_time(int(gd['hour']), 
             int(gd['minute']),
             int(gd['second']),
             int(float(u'.' + gd['fract_second'])*1000000),
             )
    return t


#
# Bindery convenience functions
#

def bind_uri(uri, rules=None, binderobj=None, prefixes=None):
    """
    Create a binding from XML retrieved from a URI
    rules - a list of bindery rule objects to fine-tune the binding
    binderobj - optional binder object to control binding details,
                the default is None, in which case a binder object
                will be created
    prefixes - dictionary mapping prefixes to namespace URIs
               the default is None
    """
    rules = rules or []
    #Create an input source for the XML
    isrc_factory = InputSource.DefaultFactory
    isrc = isrc_factory.fromUri(uri)

    if binderobj is None:
        binderobj = bindery.binder(prefixes=prefixes)
    for rule in rules:
        binderobj.add_rule(rule)

    #Now bind from the XML given in the input source
    binding = binderobj.read_xml(isrc)
    return binding


def bind_file(fname, rules=None, binderobj=None, prefixes=None):
    """
    Create a binding from XML read from a file
    rules - a list of bindery rule objects to fine-tune the binding
    binderobj - optional binder object to control binding details,
                the default is None, in which case a binder object
                will be created
    prefixes - dictionary mapping prefixes to namespace URIs
               the default is None
    """
    #Create an input source for the XML
    isrc_factory = InputSource.DefaultFactory
    #Create a URI from a filename the right way
    file_uri = Uri.OsPathToUri(fname, attemptAbsolute=1)
    binding = bind_uri(file_uri, rules=rules, binderobj=binderobj,
                       prefixes=prefixes)
    return binding

DEFAULT_URI = 'urn:bogus:unknown-resource-uri'

def bind_stream(stream, uri=None, rules=None, binderobj=None, prefixes=None):
    """
    Create a binding from XML retrieved from a file-like object
    rules - a list of bindery rule objects to fine-tune the binding
    binderobj - optional binder object to control binding details,
                the default is None, in which case a binder object
                will be created
    prefixes - dictionary mapping prefixes to namespace URIs
               the default is None
    """
    rules = rules or []
    #Create an input source for the XML
    isrc_factory = InputSource.DefaultFactory
    isrc = isrc_factory.fromStream(stream, uri or DEFAULT_URI)

    if binderobj is None:
        binderobj = bindery.binder(prefixes=prefixes)
    for rule in rules:
        binderobj.add_rule(rule)

    #Now bind from the XML given in the input source
    binding = binderobj.read_xml(isrc)
    return binding

def bind_string(st, uri=None, rules=None, binderobj=None, prefixes=None):
    """
    Create a binding from XML in string (NOT unicode) form
    rules - a list of bindery rule objects to fine-tune the binding
    binderobj - optional binder object to control binding details,
                the default is None, in which case a binder object
                will be created
    prefixes - dictionary mapping prefixes to namespace URIs
               the default is None
    """
    import cStringIO
    stream = cStringIO.StringIO(st)
    binding = bind_stream(stream, uri=None, rules=rules, binderobj=binderobj,
                       prefixes=prefixes)
    return binding


def create_document(qname=None, ns=None, content=None, attributes=None,
                    pubid=None, sysid=None):
    """
    Create a document, with optional convenience arguments to create
    top-level information items
    qname - optional QName of the document element (which will be created)
            if QName is not given, no other arguments may be given
    ns - optional namespace of the document element
    content - optional Unicode that makes up text content to be set
              as the child of the document element
    pubid - optional public ID of the doctype (to be set on the document)
    sysid - optional system ID of the doctype (to be set on the document)
    """
    if not qname:
        doc = bindery.root_base()
        return doc
    doc = bindery.root_base(doctype_name=qname, pubid=pubid, sysid=sysid)
    prefix, local = SplitQName(qname)
    doc_elem = doc.xml_element(qname, ns, attributes=attributes)
    doc.xml_append(doc_elem)
    if content:
        doc_elem.xml_append(content)
    return doc


#
#Optional bindery rules
#

class xpattern_rule_base(object):
    def __init__(self, xpatterns):
        if isinstance(xpatterns, str) or isinstance(xpatterns, unicode) :
            xpatterns = [xpatterns]
        self.xpatterns = xpatterns
        return

    def add_rule_hook(self, binder):
        binder.xpatterns.extend(self.xpatterns)
        return

    def match(self, binder):
        #print binder.event
        #print (binder.state_machine.entering_xpatterns, self.xpatterns)
        for xp in binder.state_machine.entering_xpatterns:
            if xp in self.xpatterns: return True
        return False
    
    def dom_match(self, node, binder):
        #Currently not used
        plist = PatternList(self.xpatterns, binder.prefixes)
        #not not trick acts like a cast to boolean
        context = Context(node.ownerDocument,
                          processorNss=binder.prefixes)
        return not not plist.lookup(node, context)


class simple_string_element_rule(xpattern_rule_base):
    """
    An Amara bindery rule.  Bindery rules allow developers to customize how
    XML documents are translated to Python objects.
    
    This rule is pattern based.  Elements that match the pattern will
    be bound as simple Python unicode objects, rather than full
    element objects, saving memory.
    
    There is no default pattern.  You must specify one.
    """
    event_type = saxtools.START_ELEMENT
    target_phase = bindery.PRE_INSTANCE

    def apply(self, binder):
        #FIXME: should we be checking for binder.event_completely_handled:?
        if not self.match(binder):
            return
        parent = binder.binding_stack[-1]
        if not parent: return

        (dummy, qname, ns, local, attributes) = binder.event
        prefix = qname[:qname.rindex(local)][:-1]
        ename = binder.namer.xml_to_python(qname, ns)

        #Inset a trigger for handling child characters
        def handle_char(binder):
            (dummy, text) = binder.event
            #Append current char data to any already added
            cdata = getattr(parent, ename, '') + text
            setattr(parent, ename, cdata)
            binder.event_completely_handled = True
            return
        binder.add_rule(handle_char, saxtools.CHARACTER_DATA)

        #Inset a trigger for handling child start elements
        def handle_start(binder):
            #Skip child elements
            binder.event_completely_handled = True
            return
        binder.add_rule(handle_start, saxtools.START_ELEMENT)

        #Inset a trigger for handling the matching end eleemnt
        def handle_end(binder):
            (dummy, qname, ns, local) = binder.event
            if binder.event[2:4] == (ns, local):
                binder.remove_rule(handle_start, saxtools.START_ELEMENT)
                binder.remove_rule(handle_char, saxtools.CHARACTER_DATA)
                binder.remove_rule(handle_end, saxtools.END_ELEMENT)
                binder.event_completely_handled = True
                return
            return
        binder.add_rule(handle_end, saxtools.END_ELEMENT)
        binder.event_completely_handled = True
        return


class omit_element_rule(xpattern_rule_base):
    """
    An Amara bindery rule.  Bindery rules allow developers to customize how
    XML documents are translated to Python objects.
    
    This rule is pattern based.  Elements that match the pattern will
    be ignored and not bound to any object at all, saving memory.
    
    There is no default pattern.  You must specify one.
    """
    event_type = saxtools.START_ELEMENT
    target_phase = bindery.PRE_INSTANCE

    def apply(self, binder):
        #FIXME: should we be checking for binder.event_completely_handled:?
        if not self.match(binder):
            return

        #Inset a trigger for handling child characters
        def handle_char(binder):
            #Skip child characters
            binder.event_completely_handled = True
            return
        binder.add_rule(handle_char, saxtools.CHARACTER_DATA)
        #Manage a stack of elements that match this start, so that we know
        #When we've really met our matching end element
        self.stack_depth = 0

        #Inset a trigger for handling child start elements
        def handle_start(binder):
            #Skip child elements
            binder.event_completely_handled = True
            if binder.event[2:4] == (ns, local):
                self.stack_depth += 1
            return
        binder.add_rule(handle_start, saxtools.START_ELEMENT)

        #Inset a trigger for handling the matching end eleemnt
        def handle_end(binder):
            (dummy, qname, ns, local) = binder.event
            if binder.event[2:4] == (ns, local):
                if self.stack_depth:
                    self.stack_depth -= 1
                else:
                    binder.remove_rule(handle_start, saxtools.START_ELEMENT)
                    binder.remove_rule(handle_char, saxtools.CHARACTER_DATA)
                #Signal further rules to leave off
                binder.event_completely_handled = True
                binder.remove_rule(handle_end, saxtools.END_ELEMENT)
                return
            return
        binder.add_rule(handle_end, saxtools.END_ELEMENT)
        binder.event_completely_handled = True
        return


class preserve_attribute_details(xpattern_rule_base):
    """
    An Amara bindery rule.  Bindery rules allow developers to customize how
    XML documents are translated to Python objects.
    
    This rule is pattern based.  Elements that match the pattern
    and their descendants preserve full attribute info.
    
    The default pattern is '*', meaning all elements.
    """
    event_type = saxtools.START_ELEMENT
    target_phase = bindery.POST_INSTANCE

    def __init__(self, xpatterns=None):
        import warnings
        warnings.warn("You probably no longer need to use preserve_attribute_details.  All attribute info is now preserved by default.  If you really think you need this rule, please post to the list why, because it will soon be removed.", DeprecationWarning, 2)

        if not xpatterns:
            xpatterns = [u'*']
        xpattern_rule_base.__init__(self, xpatterns)
        #Track how deep we are within a matched element event
        #0 means not within a matched element event
        self.current_match_depth = 0
        return
    
    def apply(self, binder):
        #FIXME: should we be checking for binder.event_completely_handled:?
        if not self.match(binder):
            return

        if self.current_match_depth:
            return

        self.current_match_depth = 1
        #The match depth tells us when we meet our matching end element
        (dummy, qname, ns, local, attributes) = binder.event
        #Inset a trigger for handling contained matching elements
        def handle_start(binder):
            (dummy, qname, ns, local, attributes) = binder.event
            #Presume that a previous rule handler has added
            #The current instance to the stack
            instance = binder.binding_stack[-1]
            #key_list = [ binder.namer.xml_to_python() for qn in attributes.getQNames() ]
            attr_list = [
                (attributes.getNameByQName(qn)
                 + (qn[:qn.find(':')+1][:-1], attributes.getValueByQName(qn))
                ) for qn in attributes.getQNames()
                ]
            instance.xml_attributes = dict(zip(attributes.getQNames(), attr_list))
            #print "start", self.current_match_depth, binder.event[2:4], instance.__class__, binder.binding_stack, instance.xml_attributes
            self.current_match_depth += 1
            return
        #Rule must be added to the end, after the default (which does the usual
        #element handling)
        handle_start.target_phase = bindery.POST_INSTANCE
        binder.add_rule(handle_start, saxtools.START_ELEMENT)
        #binder.rules[saxtools.START_ELEMENT].append(handle_start)
        #print binder.rules
        #Even though we've added it to the rules list, it won't be immediately executed
        handle_start(binder)

        #Inset a trigger for handling the matching end eleemnt
        def handle_end(binder):
            #print "end", self.current_match_depth, binder.event[2:4], binder.rules
            self.current_match_depth -= 1
            if self.current_match_depth == 1:
                #Back to original matching end element
                self.current_match_depth = 0
                binder.remove_rule(handle_start, saxtools.START_ELEMENT)
                binder.remove_rule(handle_end, saxtools.END_ELEMENT)
                return
            return
        binder.add_rule(handle_end, saxtools.END_ELEMENT)
        binder.event_completely_handled = False
        return


class ws_strip_element_rule(xpattern_rule_base, bindery.default_element_rule):
    """
    An Amara bindery rule.  Bindery rules allow developers to customize how
    XML documents are translated to Python objects.
    
    This rule is pattern based.  Elements that match the pattern and
    descendants will have text children stripped if they are pure whitespace.
    In other words
    <a> <b/> <c/> </a>
    will end up with the same binding as
    <a> <b/> <c/> </a>
    but not
    <a> <b/> x <c/> </a> <!-- ' x ' is not pure whirespace -->
    Stripping whitespace saves memory and can simplify resulting bindings,
    but be sure the whitespace doesn't have a significant meeaning in the
    document.
    
    The default pattern is '*', meaning all elements.
    """
    event_type = saxtools.START_ELEMENT
    target_phase = bindery.PRE_INSTANCE
    
    def __init__(self, xpatterns=None):
        if not xpatterns:
            xpatterns = [u'*']
        xpattern_rule_base.__init__(self, xpatterns)
        return

    def apply(self, binder):
        if not self.match(binder):
            return
        if binder.event_completely_handled:
            #Then another rule has already created an instance
            return
        self.stack_depth = 0
        
        #Inset a trigger for handling child characters
        def handle_char(binder):
            if binder.event_completely_handled:
                #Then another rule has already created an instance
                return
            parent = binder.binding_stack[-1]
            if not parent: return
            (dummy, text) = binder.event
            if text.strip():
                parent.xml_children.append(text)
            binder.event_completely_handled = True
            return
        handle_char.target_phase = bindery.PRE_INSTANCE

        #Inset a trigger for handling the matching end eleemnt
        def handle_end(binder):
            self.stack_depth -= 1
            if binder.event_completely_handled:
                return
            #if binder.binding_stack[-1] is instance:
            binder.binding_stack.pop()
            binder.event_completely_handled = True
            if not self.stack_depth:
                binder.remove_rule(handle_end, saxtools.END_ELEMENT)
                binder.remove_rule(handle_char, saxtools.CHARACTER_DATA)
                binder.remove_rule(handle_start, saxtools.START_ELEMENT)
            return
        handle_end.target_phase = bindery.PRE_INSTANCE
        #binder.event_completely_handled = True

        #Inset a trigger for handling child start elements
        def handle_start(binder):
            parent = binder.binding_stack[-1]
            if not parent: return
            self.stack_depth += 1
            (dummy, qname, ns, local, attributes) = binder.event
            prefix = qname[:qname.rindex(local)][:-1]
            ename = binder.namer.xml_to_python(local, ns, prefix)

            instance = bindery.create_element(binder.namer, qname, ns, ename)
            bindery.bind_attributes(instance, parent, ename, binder)
            instance = bindery.bind_instance(instance, parent)
            binder.binding_stack.append(instance)
            binder.event_completely_handled = True
            return
        handle_start.target_phase = bindery.PRE_INSTANCE
        binder.add_rule(handle_start, saxtools.START_ELEMENT)
        binder.add_rule(handle_char, saxtools.CHARACTER_DATA)
        binder.add_rule(handle_end, saxtools.END_ELEMENT)
        handle_start(binder)

        return


def infer_data_from_string(value):
    data_value = None
    try:
        data_value = int(value)
    except ValueError:
        try:
            data_value = float(value)
        except ValueError:
            data_value = parse_isodate(value)
            if not data_value:
                data_value = parse_isotime(value)
    return data_value


class type_inference(xpattern_rule_base):
    """
    An Amara bindery rule.  Bindery rules allow developers to customize how
    XML documents are translated to Python objects.
    
    This rule is pattern based.  Children of elements that match
    the pattern are checked to see if they could be a more specialized
    type, such as int, float or date
    
    The default pattern is '*', meaning all elements.
    """
    event_type = saxtools.START_ELEMENT
    target_phase = bindery.POST_INSTANCE
    ISODATE_PAT = re.compile('')

    def __init__(self, xpatterns=None):
        if not xpatterns:
            xpatterns = [u'*']
        xpattern_rule_base.__init__(self, xpatterns)
        #Track how deep we are within a matched element event
        #0 means not within a matched element event
        self.current_match_depth = 0
        return
    
    def apply(self, binder):
        #FIXME: should we be checking for binder.event_completely_handled:?
        if not self.match(binder):
            return

        if self.current_match_depth:
            return

        self.current_match_depth = 1
        #The match depth tells us when we meet our matching end element
        (dummy, qname, ns, local, attributes) = binder.event
        #Inset a trigger for handling contained matching elements
        def handle_start(binder):
            (dummy, qname, ns, local, attributes) = binder.event
            #Presume that a previous rule handler has added
            #The current instance to the stack
            instance = binder.binding_stack[-1]
            #key_list = [ binder.namer.xml_to_python() for qn in attributes.getQNames() ]
            if hasattr(instance, "xml_attributes"):
                for attr, (qname, ns) in instance.xml_attributes.items():
                    value = getattr(instance, attr)
                    data_value = infer_data_from_string(value)
                    if data_value is not None:
                        setattr(instance, attr, data_value)
            #print "start", self.current_match_depth, binder.event[2:4], instance.__class__, binder.binding_stack, instance.xml_attributes
            self.current_match_depth += 1
            return
        #Rule must be added to the end, after the default (which does the usual
        #element handling)
        handle_start.target_phase = bindery.POST_INSTANCE
        binder.add_rule(handle_start, saxtools.START_ELEMENT)
        #binder.rules[saxtools.START_ELEMENT].append(handle_start)
        #print binder.rules
        #Even though we've added it to the rules list, it won't be immediately executed
        handle_start(binder)

        #Inset a trigger for handling the matching end eleemnt
        def handle_end(binder):
            (dummy, qname, ns, local) = binder.event
            prefix = qname[:qname.rindex(local)][:-1]
            ename = binder.namer.xml_to_python(qname, ns)

            #print "end", self.current_match_depth, binder.event[2:4], binder.rules
            instance = binder.binding_stack[-1]
            #Only infer a type for an element if it has all text node children
            #And no attributes
            if ( not hasattr(instance, "xml_attributes") and
                 not [ child for child in instance.xml_children
                             if not isinstance(child, unicode) ] ):
                #No child elements
                value = u"".join(instance.xml_children)
                data_value = infer_data_from_string(value)
                if data_value is None:
                    data_value = value
                parent = instance.xml_parent
                if len(list(getattr(parent, ename))) == 1:
                    parent.__dict__[ename] = data_value
                    i = parent.xml_children.index(instance)
                    parent.xml_children[i] = data_value
            self.current_match_depth -= 1
            if self.current_match_depth == 1:
                #Back to original matching end element
                self.current_match_depth = 0
                binder.remove_rule(handle_start, saxtools.START_ELEMENT)
                binder.remove_rule(handle_end, saxtools.END_ELEMENT)
                return
            return
        binder.add_rule(handle_end, saxtools.END_ELEMENT)
        binder.event_completely_handled = False
        return


#
# Pushbind
#

from harpia.amara import saxtools
from xml import sax

def pushbind(xpatterns, source=None, string=None, prefixes=None,
             rules=None, lookahead=2):
    """
    Generator that yields subtrees of Python object bindings from XML
    according to the given pattern.  The patterns are must be XSLT patterns
    matching elements.
    
    Example: for an xml document
    
    XML = '<a> <b><c/></b> <b><c/></b> <b><c/></b> </a>'
    
    pushbind('b', string=XML)
    Will return a generator that yields the first, second and third b
    element in turn as Python objects containing the full subtree.
    
    Warning: this function uses threads and only works in Python distros
    with threading support.

    lookahead - how far ahead the SAX engine looks for events before waiting
    for the user to request another subtree from the generator.  Must be 0 or
    at least 2.  0 means the SAX engine will just load and queue up object for
    the entire file in the background.
    """
    #Saved some pondering by reference to Jimmy Retzlaff
    #http://groups-beta.google.com/group/comp.lang.python/msg/982bd32c08450352
    if lookahead == 2: lookahead = 1
    import Queue
    try:
        import threading
    except ImportError:
        import dummy_threading as threading
    queue = Queue.Queue(lookahead)
    def handle_chunk(docfrag):
        queue.put(docfrag)
        return

    #Create an instance of the chunker
    handler = saxbind_chunker(xpatterns=xpatterns, prefixes=prefixes,
        chunk_consumer=handle_chunk, rules=rules
    )

    def launch_sax():
        parser = sax.make_parser()

        #The chunker is the SAX handler
        parser.setContentHandler(handler)
        parser.setFeature(sax.handler.feature_namespaces, 1)
        if source:
            parser.parse(source)
        else:
            from cStringIO import StringIO
            parser.parse(StringIO(string))
        queue.put(None)  #Sentinel to mark that we're done
        return

    sax_thread = threading.Thread(target=launch_sax)
    sax_thread.setDaemon(True)
    sax_thread.start()

    while True:
        elem = queue.get()
        if elem:
            yield elem
        else:
            break
    return


class saxbind_chunker(bindery.binder, saxtools.sax2dom_chunker):
    """
    Note: Ignores nodes prior to the document element, such as PIs and
    text nodes.  Collapses CDATA sections into plain text
    Only designed to work if you set the feature
      sax.handler.feature_namespaces
    to 1 on the parser you use.

    xpatterns - list of XSLT Patterns.  Only portions of the
        tree within these patterns will be instantiated as DOM (as
        chunks fed to chunk_consumer in sequence)
        If None (the default, a DOM node will be created representing
        the entire tree.

    prefixes - a dictionary of prefix -> namespace name mappings used to
        interpret XPatterns
    
    chunk_consumer - a callable object taking an XML root object.  It will be
        invoked as each chunk is prepared.
    """
    def __init__(self,
                 xpatterns=None,
                 prefixes=None,
                 chunk_consumer=None,
                 rules=None,
                 ):
        bindery.binder.__init__(self, prefixes)
        #Add patterns form the push match specs
        if isinstance(xpatterns, str) or isinstance(xpatterns, unicode) :
            xpatterns = [xpatterns]
        self.xpatterns.extend(xpatterns)
        rules = rules or []
        for rule in rules:
            self.add_rule(rule)
        prefixes = prefixes or {}
        #print self.xpatterns
        self.state_machine = saxtools.xpattern_state_manager(self.xpatterns, prefixes)
        self._chunk_consumer = chunk_consumer
        return

    #Overridden ContentHandler methods
    def startDocument(self):
        bindery.binder.startDocument(self)
        return

    def endDocument(self):
        bindery.binder.endDocument(self)
        return

    def startElementNS(self, name, qname, attribs):
        (ns, local) = name
        qname = self.name_to_qname(name)
        #print "startElementNS", (self, name, qname, attribs)
        self.state_machine.event(1, ns, local)
        if not self.state_machine.status():
            return
        self.event = (saxtools.START_ELEMENT, qname, ns, local, attribs)
        self.apply_rules()
        return

    def endElementNS(self, (ns, local), qname):
        qname = self.name_to_qname((ns, local))
        self.state_machine.event(0, ns, local)
        if not self.state_machine.status():
            #print (self.state_machine._state, self.state_machine.entering_xpatterns, self.state_machine.leaving_xpatterns)
            if (self._chunk_consumer and
                self.state_machine.leaving_xpatterns):
                self.event = (saxtools.END_ELEMENT, qname, ns, local)
                self.apply_rules()
                self.event = (saxtools.END_DOCUMENT,)
                self.apply_rules()
                root = self.binding_stack[0]
                elem = root.xml_children[-1]
                del root
                elem.xmlns_prefixes = self.prefixes
                elem.xml_parent = None
                self._chunk_consumer(elem)
                #Start all over with a new container so the old
                #One's memory can be reclaimed
                self.binding_stack = []
                self.event = (saxtools.START_DOCUMENT,)
                self.apply_rules()
            return
        self.event = (saxtools.END_ELEMENT, qname, ns, local)
        self.apply_rules()
        return

    def characters(self, chars):
        bindery.binder.characters(self, chars)
        return


