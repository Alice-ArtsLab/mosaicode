#!/usr/bin/env python
"""
Python compiler from DTLL (ISO DSDL Part 5: Datatypes) to a Python data types script
"""

import os
import re
import sys
import codecs
import optparse
import cStringIO
from xml import sax
from amara import domtools
from Ft.Xml.Domlette import GetAllNs
from Ft.Xml.Domlette import NonvalidatingReader

from xml.dom import EMPTY_NAMESPACE as NULL_NAMESPACE
from xml.dom import EMPTY_PREFIX as NULL_PREFIX

DTLL_NS = "http://www.jenitennison.com/datatypes"
WXSDT_NS = "http://www.w3.org/2001/XMLSchema-datatypes"

#FIXME: Use 4Suite L10N
def _(t): return t
NAMED_PATTERN_PAT = re.compile(r'\(\?\[(\w+)\]')


TOP_SKEL = u'''\
#Warning: this is an auto-generated file.  Do not edit unless you're
#sure you know what you're doing

import sys
import re
import codecs
'''

MAIN_SKEL = u'''\
BASE_URI = '%(ns)s'
'''

DT_CLASS_SKEL = u'''\
class %s(name)Type:
    self._name = %(name)s
'''

DT_REGEX_SKEL = u'''\
    regex = re.compile(%(regex)s)
    def __init__(self, value):
        m = self.regex.match(value)
        if not m:
            raise ValueError('Value does not conform to specified regex for data type %%s'%%(self._name))
        #Extract named patterns
        self.__dict__.update(m.groupdict())
        return
'''

DT_NO_REGEX_SKEL = u'''\
    def __init__(self, value):
        return
'''


class dtll_processor:
    def __init__(self, output_stem):
        self.reset()
        self.output_stem = output_stem
        return

    def reset(self):
        self.prefixes = {'dtll': DTLL_NS, 'wxs': WXSDT_NS}
        #Maps each data type namespace to one module of Python output
        self.outputs = {}
        return

    def execute(self, dtlldoc):
        for datatype in domtools.get_elements_by_tag_name_ns(dtlldoc, DTLL_NS, u'datatype'):
            self.handle_datatype(datatype)
        return

    def write_files(self):
        module_count = 1
        for ns, cstring in self.outputs.items():
            fout = open(self.output_stem + str(module_count) + '.py', 'w')
            fout.write(cstring.getvalue())
            module_count += 1
        return

    def handle_datatype(self, datatype):
        qname = datatype.getAttributeNS(NULL_PREFIX, u'name')
        prefix = qname[:qname.find(':') + 1][:-1] or NULL_PREFIX
        local = qname[qname.find(':')+1:]
        namespace = None
        if prefix:
            #Specified data type namespace by using a qname
            namespace = self.prefixes.get(prefix)
        if not namespace:
            #Specified data type namespace by in-scope namespaces
            namespace = GetAllNs(datatype)[prefix]
        output = self.outputs.setdefault(namespace, cStringIO.StringIO())
        output.write(TOP_SKEL)
        skel_params = {'ns': namespace}
        output.write(MAIN_SKEL%skel_params)
        skel_params = {'name': local}
        output.write(DT_CLASS_SKEL%skel_params)
        
        for parse in domtools.get_elements_by_tag_name_ns(datatype, DTLL_NS, u'parse'):
            self.handle_parse(parse, output)
        return
    
    def handle_parse(self, parse, output):
        regexen = list(domtools.get_elements_by_tag_name_ns(parse, DTLL_NS, u'regex'))
        if regexen:
            regex = python_regex(domtools.string_value(regexen[0]))
            skel_params = {'regex': regex}
            output.write(DT_REGEX_SKEL%skel_params)
        else:
            output.write(DT_NO_REGEX_SKEL)
        return
    

def python_regex(dtllregex):
    '''
    Convert a DTLL regex to a Python/Perl regex
    '''
    return NAMED_PATTERN_PAT.subn(lambda m: '(?P<'+m.group(1)+'>', dtllregex)[0]


def run(dtll_doc, output_stem, prep_for_test=0):
    #global BOTTOM_SKEL
    #if prep_for_test:
    #    BOTTOM_SKEL = MAIN_SKEL + TEST_SCRIPT_SKEL
    #else:
    #    BOTTOM_SKEL = MAIN_SKEL
    proc = dtll_processor(output_stem)
    proc.execute(dtll_doc)
    proc.write_files()
    return


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def command_line(args):
    from optparse import OptionParser
    usage = "%prog [options] dtll-file"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--dt-module-prefix",
                      action="store", type="string", dest="dt_modname_stem",
                      help="file name prefix for data type modules to be generated", metavar="FILE")
    parser.add_option("--test",
                      action="store_true", dest="test_ready", default=0,
                      help="generate hooks for unit tests in the data type")
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
            dtll_fname = ARGS[1]
        except KeyboardInterrupt:
            pass
        except:
             raise Usage(optparser.format_help())
        enc, dec, inwrap, outwrap = codecs.lookup('utf-8')
        output_stem = OPTIONS.dt_modname_stem
        if not output_stem:
            output_stem = os.path.splitext(dtll_fname)[0] + '-datatypes'
        if dtll_fname == '-':
            dtllf = sys.stdin
        else:
            dtllf = open(dtll_fname, 'r')
        dtll_doc = NonvalidatingReader.parseStream(dtllf, 'http://example.com')
        run(dtll_doc, output_stem, OPTIONS.test_ready)
    except Usage, err:
        print >>sys.stderr, err.msg
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))

