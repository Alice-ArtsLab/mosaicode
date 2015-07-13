#!/usr/bin/env python
"""
Python compiler from ISO Schematron to a Python validator script
"""

import os
import sys
import codecs
import optparse
import cStringIO
from xml import sax
from amara import saxtools


_ = lambda x:x.encode('utf-8')

SCRIPT_HEADER = u'#!/usr/bin/env python'

TOP_SKEL = u'''\
%s
#Warning: this is an auto-generated file.  Do not edit unless you're
#sure you know what you're doing

import sys
import codecs
import optparse
from Ft.Xml.Xslt import PatternList, parser
from Ft.Xml.Xslt import Stylesheet
from Ft.Xml.XPath import Compile as CompileXPath
from Ft.Xml.XPath.Context import Context as XPathContext
from Ft.Xml.Xslt.XsltContext import XsltContext
from Ft.Xml.Domlette import NonvalidatingReader
from Ft.Xml.XPath import Conversions
from Ft.Xml.XPath import Util
from Ft.Xml.XPath import CoreFunctions

from Ft.Xml.Xslt.XmlWriter import XmlWriter
from Ft.Xml.Xslt.OutputParameters import OutputParameters
from Ft.Lib import Uri

from amara import domtools

XPATTERN_PARSER = parser.new()
del parser

'''%SCRIPT_HEADER

MAIN_SKEL = u'''

class faux_xslt_proc(Stylesheet.StylesheetElement):
    #Pretends to be an XSLT processor for processing keys
    def __init__(self, doc):
        self.namespaces = NSS
        self._keys = [ (Util.ExpandQName(k[0], doc), k[1], k[2]) for k in KEYS ]
        self.keys = {}
        self.initialFunctions = {}
        self.stylesheet = self
        #Update all the keys for all documents in the context
        #Note: 4Suite uses lazy key eval.  Consider emulating this
        for key in self._keys:
            Stylesheet.StylesheetElement.updateKey(self, doc, key[0], self)
        #print self.keys
        return


def validate(xmlf, reportf):
    global WRITER
    oparams = OutputParameters()
    oparams.indent = 'yes'
    WRITER = XmlWriter(oparams, reportf)
    WRITER.startDocument()

    WRITER.text(u'Processing schema: ')
    WRITER.text(%(title)s)
    WRITER.text(u'\\n\\n')
    
    if xmlf == '-':
        doc = NonvalidatingReader.parseStream(sys.stdin, 'urn:stron-candidate-dummy')
    elif not isinstance(xmlf, str):
        doc = NonvalidatingReader.parseStream(xmlf, 'urn:stron-candidate-dummy')
    else:
        try:
            doc = NonvalidatingReader.parseUri(xmlf)
        except ValueError:
            doc = NonvalidatingReader.parseUri(Uri.OsPathToUri(xmlf))

    global key_handler
    key_handler = None
    #Pre-process keys, if any
    if KEYS:
        key_handler = faux_xslt_proc(doc)
    #for kname, (kuse, kmatch) in KEYS.items:
    
    #Main rule-processing loop
    if PATTERNS:
        for pat in PATTERNS:
            #if not pat[2].keys():
            #    WRITER.text(_(u'Pattern context not given'))
            plist = PatternList(pat[2].keys(), NSS)
            WRITER.text(u'Processing pattern: ')
            WRITER.text(pat[0] or u'[unnamed]')
            WRITER.text(u'\\n\\n')
            for node in domtools.doc_order_iter(doc):
                #FIXME: this is a 4Suite bug work-around.  At some point remove
                #The redundant context setting
                matches = plist.lookup(
                    node, context=XsltContext(node, processorNss=NSS)
                    )
                if matches:
                    func = pat[2][matches[0]]
                    func(node)
    else:
        #Second parameter is a dictionary of prefix to namespace mappings
        plist = PatternList(CONTEXTS.keys(), {})
        for node in domtools.doc_order_iter(doc):
            #FIXME: this is a 4Suite bug work-around.  At some point remove
            #The redundant context setting
            matches = plist.lookup(node, context=XsltContext(node, processorNss=NSS))
            if matches:
                func = CONTEXTS[matches[0]]
                func(node)
    WRITER.endDocument()
    return


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def command_line(args):
    from optparse import OptionParser
    usage = "%%prog [options] xml-file\\nxml-file is the XML file to be validated"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--val-output",
                      action="store", type="string", dest="val_output",
                      help="generate the validation report file FILE (XML external parsed entity format)", metavar="FILE")
    global OPTIONS, ARGS
    (OPTIONS, ARGS) = parser.parse_args(args)
    return parser

def main(argv=[__name__]):
    #Ideas borrowed from http://www.artima.com/forums/flat.jsp?forum=106&thread=4829
    if argv is None:
        argv = sys.argv
    try:
        try:
            optparser = command_line(argv)
            candidate_file = ARGS[1]
        except KeyboardInterrupt:
            pass
        except:
             raise Usage(optparser.format_help())
        enc, dec, inwrap, outwrap = codecs.lookup('utf-8')
        fout = OPTIONS.val_output
        if fout:
            fout = open(fout, 'w')
        else:
            fout = sys.stdout
        validate(candidate_file, outwrap(fout))
    except Usage, err:
        print >>sys.stderr, err.msg
        return 2

'''

SCRIPT_SKEL = u'''
if __name__ == "__main__":
    sys.exit(main(sys.argv))

'''

TEST_SCRIPT_SKEL = u'''
if __name__ == "__main__":
    if not TEST:
        sys.exit(main(sys.argv))

'''

RULE_SKEL = u'''
def rule%(rcount)s(node):
    #For context XPattern %(context)s
    vars = {}
'''

ASSERT_SKEL = u'''\
    expr = CompileXPath(%(test)s)
    xpath_ctx = XsltContext(node, processor=key_handler, processorNss=NSS, varBindings=vars)
    if not Conversions.BooleanValue(expr.evaluate(xpath_ctx)):
'''

REPORT_SKEL = u'''\
    expr = CompileXPath(%(test)s)
    xpath_ctx = XsltContext(node, processor=key_handler, processorNss=NSS, varBindings=vars)
    if Conversions.BooleanValue(expr.evaluate(xpath_ctx)):
'''

DIAG_SKEL = u'''\
def diag%(diagcount)i(xpath_ctx):
    #Diagnostic named %(id)s
'''

EMIT_RULE_PATTERN_ITEM = u'''\
  XPATTERN_PARSER.parse(%(pat)s): %(func)s,
'''

EMIT_DIAG_ID_ITEM = u'''\
  %(id)s: %(func)s,
'''

EMIT_START_ELEM_SKEL = u'''\
%(indent)sWRITER.startElement(%(qname)s, %(ns)s)
'''

EMIT_END_ELEM_SKEL  = u'''\
%(indent)sWRITER.endElement(%(qname)s, %(ns)s)
'''

EMIT_ATTRIBUTE_SKEL  = u'''\
%(indent)sWRITER.attribute(%(qname)s, %(ns)s, %(val)s)
'''

EMIT_TEXT_SKEL  = u'''\
%(indent)sWRITER.text(%(text)s)
'''

EMIT_NAME_SKEL  = u'''\
%(indent)sexpr = CompileXPath(%(path)s)
%(indent)sname = CoreFunctions.Name(xpath_ctx, expr.evaluate(xpath_ctx))
%(indent)sWRITER.text(name)
'''

EMIT_VALUE_OF_SKEL  = u'''\
%(indent)sexpr = CompileXPath(%(select)s)
%(indent)sval = Conversions.StringValue(expr.evaluate(xpath_ctx))
%(indent)sWRITER.text(val)
'''


STRON_NS = 'http://www.ascc.net/xml/schematron'

#Indices into the pattern information tuple
RULE_FUNCTIONS = 2
PAT_IS_ABSTRACT = 3
RULE_CONTEXTS = 4

#The marker within an abstract pattern template for a chunk to be parameterized
ABSPAT_DELIMITER = u'\u0001'    #A char that cannot appear in XML


class stron_consumer:
    """
    Encapsulation of a set of semi-co-routines designed to handle SAX
    Events from Schematron
    """
    def __init__(self, output):
        self.top_dispatcher = {
            (saxtools.START_ELEMENT, STRON_NS, u'schema'):
            self.handle_schema,
            }
        self.output = output
        self.rule_contexts = {}
        self.rule_count = 1
        self.diag_ids = {}
        self.diag_count = 1
        self.event = None
        #Default version is ISO
        self.version = 'ISO'
        self.schema_title = u''
        self.patterns = []
        self.abstract_patterns = {}
        self.curr_pattern = None
        self.nss = {}
        self.keys = []
        self.vars = {}
        return

    def handle_schema(self, end_condition):
        dispatcher = {
            (saxtools.START_ELEMENT, STRON_NS, u'title'):
            self.handle_title,
            (saxtools.START_ELEMENT, STRON_NS, u'pattern'):
            self.handle_pattern,
            (saxtools.START_ELEMENT, STRON_NS, u'rule'):
            self.handle_rule,
            (saxtools.START_ELEMENT, STRON_NS, u'diagnostic'):
            self.handle_diagnostic,
            (saxtools.START_ELEMENT, STRON_NS, u'ns'):
            self.handle_ns,
            (saxtools.START_ELEMENT, STRON_NS, u'key'):
            self.handle_key,
            }
        #Initial call corresponds to the start schema element
        #Update the version, if specified
        self.version = self.params.get((None, 'version'))
        self.output.write(TOP_SKEL)
        curr_gen = None
        yield None
        while not self.event == end_condition:
            #print "schema", self.event
            curr_gen = saxtools.tenorsax.event_loop_body(dispatcher, curr_gen, self.event)
            yield None
        #Element closed.  Wrap up
        self.output.write(u'\nPATTERNS = [\n')
        for (pname, pid, pcontexts) in self.patterns:
            self.output.write(u'(\n %s, %s, {\n'%(repr(pname), repr(pid)))
            for rc in pcontexts:
                self.output.write(EMIT_RULE_PATTERN_ITEM%{'pat': repr(rc), 'func': pcontexts[rc]})
            self.output.write(u'}),\n')
        self.output.write(u']\n')
        self.output.write(u'\nCONTEXTS = {\n')
        for rc in self.rule_contexts:
            self.output.write(EMIT_RULE_PATTERN_ITEM%{'pat': repr(rc), 'func': self.rule_contexts[rc]})
        self.output.write(u'}\n')
        self.output.write(u'\nDIAGNOSTICS = {\n')
        for id in self.diag_ids:
            self.output.write(EMIT_DIAG_ID_ITEM%{'id': repr(id), 'func': self.diag_ids[id]})
        self.output.write(u'}\n')
        self.output.write(u'\nNSS = {\n')
        for prefix in self.nss:
            ns = self.nss[prefix]
            self.output.write(u'%(prefix)s: %(ns)s, '%{'prefix': repr(prefix), 'ns': ns and repr(ns)})
        self.output.write(u'}\n')
        self.output.write(u'\nKEYS = [\n')
        for n, m, u in self.keys:
            self.output.write(u'(%(n)s, %(m)s, CompileXPath(%(u)s)),'%{'n': repr(n), 'm': repr(m), 'u': repr(u)})
        self.output.write(u']\n')
        
        self.output.write(BOTTOM_SKEL%{'title': repr(self.schema_title)})
        raise StopIteration

    def handle_pattern(self, end_condition):
        name = self.params.get((None, 'name'))
        id_ = self.params.get((None, 'id'))
        abstract = self.params.get((None, 'abstract')) == u'true'
        isa = self.params.get((None, 'is-a'))
        self.curr_pattern = (name, id_, {}, abstract, [])
        if abstract:
            save_output = self.output
            self.output = cStringIO.StringIO()
        if isa:
            params = {}
        def handle_param(end_condition):
            formal = self.params.get((None, 'formal'))
            actual = self.params.get((None, 'actual'))
            if formal is None or actual is None:
                raise ValueError(_(u"sch:param must have 'formal' and 'actual' attributes."))
            params[formal] = actual
            yield None
            return
        dispatcher = {
            (saxtools.START_ELEMENT, STRON_NS, 'rule'):
            self.handle_rule,
            (saxtools.START_ELEMENT, STRON_NS, 'param'):
            handle_param,
            }
        curr_gen = None
        yield None
        while not self.event == end_condition:
            #print "pattern", self.event
            curr_gen = saxtools.tenorsax.event_loop_body(dispatcher, curr_gen, self.event)
            yield None
        #Element closed.  Wrap up
        if abstract:
            #Create a closure for resolving the abstract pattern
            def resolve_abspat(
                    params, template=self.output.getvalue(),
                    rule_contexts=self.curr_pattern[RULE_CONTEXTS]):
                #print >> sys.stderr, 'Resolving abstract pattern', template, params
                rule_contexts = iter(rule_contexts)
                chunks = template.split(ABSPAT_DELIMITER)
                for count, chunk in enumerate(chunks):
                    if count % 2:
                        if chunk == '$':
                            rfunc = u'rule' + str(self.rule_count)
                            context = rule_contexts.next()
                            for formal in params:
                                context = context.replace('$'+formal, params[formal])
                            self.curr_pattern[RULE_FUNCTIONS][context] = rfunc
                            self.output.write(str(self.rule_count))
                            self.rule_count += 1
                        else:
                            for formal in params:
                                chunk = chunk.replace('$'+formal, params[formal])
                            self.output.write(repr(chunk))
                    else:
                        self.output.write(chunk)
            self.output = save_output
            self.abstract_patterns[name] = resolve_abspat
        if isa:
            #FIXME: assumes abs pattern is defined before the parameter pattern
            #Probably not a valid restriction
            resolve = self.abstract_patterns[isa]
            resolve(params)
        if not self.curr_pattern[PAT_IS_ABSTRACT]:
            self.patterns.append(self.curr_pattern[:3])
        self.curr_pattern = None
        raise StopIteration

    def handle_rule(self, end_condition):
        dispatcher = {
            (saxtools.START_ELEMENT, STRON_NS, 'assert'):
            self.handle_assert,
            (saxtools.START_ELEMENT, STRON_NS, 'report'):
            self.handle_report,
            (saxtools.START_ELEMENT, STRON_NS, 'let'):
            self.handle_rule_let,
            }
        context = self.params.get((None, 'context'))
        if not context:
            raise TypeError(_(u'Pattern context not given'))
        save_vars = self.vars
        if self.curr_pattern and self.curr_pattern[PAT_IS_ABSTRACT]:
            #Handle parameterization for context in abstract patterns
            marked_context = ABSPAT_DELIMITER + context + ABSPAT_DELIMITER
            self.output.write(RULE_SKEL%{'rcount': ABSPAT_DELIMITER + '$' + ABSPAT_DELIMITER, 'context': marked_context})
            self.curr_pattern[RULE_CONTEXTS].append(context)
        else:
            self.output.write(
                RULE_SKEL%{'rcount': str(self.rule_count),
                           'context': repr(context)})
            rfunc = u'rule' + str(self.rule_count)
            self.rule_contexts[context] = rfunc
            self.rule_count += 1
            self.curr_pattern[RULE_FUNCTIONS][context] = rfunc
        curr_gen = None
        yield None
        while not self.event == end_condition:
            curr_gen = saxtools.tenorsax.event_loop_body(dispatcher, curr_gen, self.event)
            yield None
        #Element closed.  Wrap up
        self.output.write(u'\n    return\n\n')
        self.vars = save_vars
        raise StopIteration

    def handle_assert(self, end_condition):
        test = self.params.get((None, 'test'))
        diagnostics = self.params.get((None, 'diagnostics'))
        #FIXME: should use NMTOKENS savvy splitter
        diagnostics = diagnostics and diagnostics.split() or []
        #We want to capture all char data and markup children, so register a
        #special handler for this purpose
        curr_gen = self.xml_repeater(' '*8)
        if self.curr_pattern and self.curr_pattern[PAT_IS_ABSTRACT]:
            #Handle parameterization for asserts in abstract patterns
            marked_test = ABSPAT_DELIMITER + test + ABSPAT_DELIMITER
            self.output.write(ASSERT_SKEL%{'test': marked_test})
        else:
            self.output.write(ASSERT_SKEL%{'test': repr(test)})
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*8, 'text': repr(u'Assertion failure:\n')})
        yield None
        while not self.event == end_condition:
            #if curr_gen: curr_gen = tenorsax.delegate(curr_gen)
            curr_gen.next()
            yield None
        #Element closed.  Wrap up
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*8, 'text': repr(u'\n')})
        for diag_id in diagnostics:
            self.output.write(u'\n%(indent)sDIAGNOSTICS[%(id)s](xpath_ctx)\n'%{'indent': ' '*8, 'id': repr(diag_id)})
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*8, 'text': repr(u'\n')})
        #del curr_gen
        raise StopIteration

    def handle_report(self, end_condition):
        test = self.params.get((None, 'test'))
        #We want to capture all char data and markup children, so register a
        #special handler for this purpose
        curr_gen = self.xml_repeater(' '*8)
        if self.curr_pattern and self.curr_pattern[PAT_IS_ABSTRACT]:
            #Handle parameterization for reports in abstract patterns
            marked_test = ABSPAT_DELIMITER + test + ABSPAT_DELIMITER
            self.output.write(REPORT_SKEL%{'test': marked_test})
        else:
            self.output.write(REPORT_SKEL%{'test': repr(test)})
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*8, 'text': repr(u'Report:\n')})
        yield None
        while not self.event == end_condition:
            curr_gen.next()
            yield None
        #Element closed.  Wrap up
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*8, 'text': repr(u'\n\n')})
        #del curr_gen
        raise StopIteration

    def handle_diagnostic(self, end_condition):
        id = self.params.get((None, 'id'))
        #We want to capture all char data and markup children, so register a
        #special handler for this purpose
        curr_gen = self.xml_repeater(' '*4)
        self.output.write(DIAG_SKEL%{'diagcount': self.diag_count, 'id': repr(id)})
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*4, 'text': repr(u'Diagnostic message:\n')})
        self.diag_ids[id] = 'diag' + str(self.diag_count)
        self.diag_count += 1
        yield None
        while not self.event == end_condition:
            curr_gen.next()
            yield None
        #Element closed.  Wrap up
        self.output.write(EMIT_TEXT_SKEL%{'indent': ' '*4, 'text': repr(u'\n')})
        self.output.write(u'\n    return\n\n')
        #del curr_gen
        raise StopIteration

    def handle_title(self, end_condition):
        yield None
        while not self.event == end_condition:
            if self.event[0] == (saxtools.CHARACTER_DATA):
                self.schema_title += self.params
            yield None

    def handle_key(self, end_condition):
        name = self.params.get((None, 'name'))
        use = self.params.get((None, 'use'))
        match = self.params.get((None, 'match'))
        self.keys.append((name, match, use))
        yield None
        return

    def handle_ns(self, end_condition):
        prefix = self.params.get((None, 'prefix'))
        ns = self.params.get((None, 'uri'))
        self.nss[prefix] = ns
        yield None
        return

    def handle_rule_let(self, end_condition):
        name = self.params.get((None, 'name'))
        value = self.params.get((None, 'value'))
        self.output.write(' '*4 + 'xpath_ctx = XsltContext(node, processor=key_handler, processorNss=NSS, varBindings=vars)\n')
        self.output.write(' '*4 + 'vars[(None, ' + repr(name) + ')] = CompileXPath(' + repr(value) + ').evaluate(xpath_ctx)\n')
        #self.vars[name] = value
        yield None
        return

    def xml_repeater(self, indent):
        #print "xml_repeater"
        while 1:
            if self.event[0] == saxtools.START_ELEMENT:
                #emph, name and value-of are special cases
                if self.event[1:3] == (STRON_NS, u'name'):
                    path = self.params.get((None, 'path'), u'.')
                    self.output.write(EMIT_NAME_SKEL%{'indent': indent, 'path': repr(path)})
                elif self.event[1:3] == (STRON_NS, u'value-of'):
                    select = self.params.get((None, 'select'))
                    self.output.write(EMIT_VALUE_OF_SKEL%{'indent': indent, 'select': repr(select)})
                elif self.event[1:3] == (STRON_NS, u'emph'):
                    self.output.write(EMIT_START_ELEM_SKEL%{'indent': indent, 'qname': repr(self.event[2]), 'ns': repr(None)})
                else:
                    #Using local name for qname for now
                    self.output.write(EMIT_START_ELEM_SKEL%{'indent': indent, 'qname': repr(self.event[2]), 'ns': repr(self.event[1])})
            if self.event[0] == saxtools.END_ELEMENT:
                if not self.event[1:3] in [(STRON_NS, u'name'), (STRON_NS, u'value-of')]:
                    self.output.write(EMIT_END_ELEM_SKEL%{'indent': indent, 'qname': repr(self.event[2]), 'ns': repr(self.event[1])})
            if self.event[0] == saxtools.CHARACTER_DATA:
                self.output.write(EMIT_TEXT_SKEL%{'indent': indent, 'text': repr(self.params)})
            yield None


def run(stron_inf, validator_outf, prep_for_test=0):

    global BOTTOM_SKEL
    if prep_for_test:
        BOTTOM_SKEL = MAIN_SKEL + TEST_SCRIPT_SKEL
    else:
        BOTTOM_SKEL = MAIN_SKEL + SCRIPT_SKEL
    parser = sax.make_parser()
    consumer = stron_consumer(validator_outf)
    handler = saxtools.tenorsax(consumer)
    parser.setContentHandler(handler)
    parser.setFeature(sax.handler.feature_namespaces, 1)
    parser.parse(stron_inf)
    return


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def command_line(args):
    from optparse import OptionParser
    usage = "%prog [options] schematron-file"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--val-script",
                      action="store", type="string", dest="stron_script",
                      help="generate the XML validator script FILE", metavar="FILE")
    parser.add_option("--test",
                      action="store_true", dest="test_ready", default=0,
                      help="generate hooks for unit tests in the validator")
    #parser.add_option("-q", "--quiet",
    #                  action="store_false", dest="verbose", default=1,
    #                  help="don't print status messages to stdout")
    global OPTIONS, ARGS
    (OPTIONS, ARGS) = parser.parse_args(args)
    return parser

        
def main(argv=[__name__]):
    #Ideas borrowed from
    # http://www.artima.com/forums/flat.jsp?forum=106&thread=4829
    if argv is None:
        argv = sys.argv
    try:
        try:
            optparser = command_line(argv)
            stron_fname = ARGS[1]
        except KeyboardInterrupt:
            pass
        except:
             raise Usage(optparser.format_help())
        enc, dec, inwrap, outwrap = codecs.lookup('utf-8')
        fout = OPTIONS.stron_script
        if not fout:
            fout = os.path.splitext(stron_fname)[0] + '-stron.' + 'py'
        fout = open(fout, 'w')
        if stron_fname == '-':
            stronf = sys.stdin
        else:
            stronf = open(stron_fname, 'r')
        run(stronf, outwrap(fout), OPTIONS.test_ready)
    except Usage, err:
        print >>sys.stderr, err.msg
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))


