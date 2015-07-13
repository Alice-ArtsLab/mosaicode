__all__ = ["DeclHandler", "LexicalHandler", 'all_features', 'all_properties', 'feature_external_ges', 'feature_external_pes', 'feature_namespace_prefixes', 'feature_namespaces', 'feature_string_interning', 'feature_validation', 'property_declaration_handler', 'property_dom_node', 'property_encoding', 'property_interning_dict', 'property_lexical_handler', 'property_xml_string']


#Snipped from xml.sax.saxlib
"""
This module contains the core classes of version 2.0 of SAX for Python.
This file provides only default classes with absolutely minimum
functionality, from which drivers and applications can be subclassed.

Many of these classes are empty and are included only as documentation
of the interfaces.

$Id: pyxml_standins.py,v 1.1.1.2 2006/03/10 12:19:20 fpterra Exp $
"""

# A number of interfaces used to live in saxlib, but are now in
# various other modules for Python 2 compatibility. If nobody uses
# them here any longer, the references can be removed

from xml.sax.handler import ErrorHandler, ContentHandler, DTDHandler, EntityResolver
from xml.sax.xmlreader import XMLReader, InputSource, Locator, IncrementalParser

#============================================================================
#
# HANDLER INTERFACES
#
#============================================================================


# ===== DECLHANDLER =====

class DeclHandler:
    """Optional SAX2 handler for DTD declaration events.

    Note that some DTD declarations are already reported through the
    DTDHandler interface. All events reported to this handler will
    occur between the startDTD and endDTD events of the
    LexicalHandler.

    To set the DeclHandler for an XMLReader, use the setProperty method
    with the identifier http://xml.org/sax/handlers/DeclHandler."""

    def attributeDecl(self, elem_name, attr_name, type, value_def, value):
        """Report an attribute type declaration.

        Only the first declaration will be reported. The type will be
        one of the strings "CDATA", "ID", "IDREF", "IDREFS",
        "NMTOKEN", "NMTOKENS", "ENTITY", "ENTITIES", or "NOTATION", or
        a list of names (in the case of enumerated definitions).

        elem_name is the element type name, attr_name the attribute
        type name, type a string representing the attribute type,
        value_def a string representing the default declaration
        ('#IMPLIED', '#REQUIRED', '#FIXED' or None). value is a string
        representing the attribute's default value, or None if there
        is none."""

    def elementDecl(self, elem_name, content_model):
        """Report an element type declaration.

        Only the first declaration will be reported.

        content_model is the string 'EMPTY', the string 'ANY' or the content
        model structure represented as tuple (separator, tokens, modifier)
        where separator is the separator in the token list (that is, '|' or
        ','), tokens is the list of tokens (element type names or tuples
        representing parentheses) and modifier is the quantity modifier
        ('*', '?' or '+')."""

    def internalEntityDecl(self, name, value):
        """Report an internal entity declaration.

        Only the first declaration of an entity will be reported.

        name is the name of the entity. If it is a parameter entity,
        the name will begin with '%'. value is the replacement text of
        the entity."""

    def externalEntityDecl(self, name, public_id, system_id):
        """Report a parsed entity declaration. (Unparsed entities are
        reported to the DTDHandler.)

        Only the first declaration for each entity will be reported.

        name is the name of the entity. If it is a parameter entity,
        the name will begin with '%'. public_id and system_id are the
        public and system identifiers of the entity. public_id will be
        None if none were declared."""



# ===== LEXICALHANDLER =====

class LexicalHandler:
    """Optional SAX2 handler for lexical events.

    This handler is used to obtain lexical information about an XML
    document, that is, information about how the document was encoded
    (as opposed to what it contains, which is reported to the
    ContentHandler), such as comments and CDATA marked section
    boundaries.

    To set the LexicalHandler of an XMLReader, use the setProperty
    method with the property identifier
    'http://xml.org/sax/handlers/LexicalHandler'. There is no
    guarantee that the XMLReader will support or recognize this
    property."""

    def comment(self, content):
        """Reports a comment anywhere in the document (including the
        DTD and outside the document element).

        content is a string that holds the contents of the comment."""

    def startDTD(self, name, public_id, system_id):
        """Report the start of the DTD declarations, if the document
        has an associated DTD.

        A startEntity event will be reported before declaration events
        from the external DTD subset are reported, and this can be
        used to infer from which subset DTD declarations derive.

        name is the name of the document element type, public_id the
        public identifier of the DTD (or None if none were supplied)
        and system_id the system identfier of the external subset (or
        None if none were supplied)."""

    def endDTD(self):
        "Signals the end of DTD declarations."

    def startEntity(self, name):
        """Report the beginning of an entity.

        The start and end of the document entity is not reported. The
        start and end of the external DTD subset is reported with the
        pseudo-name '[dtd]'.

        Skipped entities will be reported through the skippedEntity
        event of the ContentHandler rather than through this event.

        name is the name of the entity. If it is a parameter entity,
        the name will begin with '%'."""

    def endEntity(self, name):
        """Reports the end of an entity. name is the name of the
        entity, and follows the same conventions as for
        startEntity."""

    def startCDATA(self):
        """Reports the beginning of a CDATA marked section.

        The contents of the CDATA marked section will be reported
        through the characters event."""

    def endCDATA(self):
        "Reports the end of a CDATA marked section."

#
#From xml.sax.handler
#
#============================================================================
#
# CORE FEATURES
#
#============================================================================

feature_namespaces = "http://xml.org/sax/features/namespaces"
# true: Perform Namespace processing (default).
# false: Optionally do not perform Namespace processing
#        (implies namespace-prefixes).
# access: (parsing) read-only; (not parsing) read/write

feature_namespace_prefixes = "http://xml.org/sax/features/namespace-prefixes"
# true: Report the original prefixed names and attributes used for Namespace
#       declarations.
# false: Do not report attributes used for Namespace declarations, and
#        optionally do not report original prefixed names (default).
# access: (parsing) read-only; (not parsing) read/write

feature_string_interning = "http://xml.org/sax/features/string-interning"
# true: All element names, prefixes, attribute names, Namespace URIs, and
#       local names are interned using the built-in intern function.
# false: Names are not necessarily interned, although they may be (default).
# access: (parsing) read-only; (not parsing) read/write

feature_validation = "http://xml.org/sax/features/validation"
# true: Report all validation errors (implies external-general-entities and
#       external-parameter-entities).
# false: Do not report validation errors.
# access: (parsing) read-only; (not parsing) read/write

feature_external_ges = "http://xml.org/sax/features/external-general-entities"
# true: Include all external general (text) entities.
# false: Do not include external general entities.
# access: (parsing) read-only; (not parsing) read/write

feature_external_pes = "http://xml.org/sax/features/external-parameter-entities"# true: Include all external parameter entities, including the external
#       DTD subset.
# false: Do not include any external parameter entities, even the external
#        DTD subset.
# access: (parsing) read-only; (not parsing) read/write

all_features = [feature_namespaces,
                feature_namespace_prefixes,
                feature_string_interning,
                feature_validation,
                feature_external_ges,
                feature_external_pes]


#============================================================================
#
# CORE PROPERTIES
#
#============================================================================

property_lexical_handler = "http://xml.org/sax/properties/lexical-handler"
# data type: xml.sax.sax2lib.LexicalHandler
# description: An optional extension handler for lexical events like comments.
# access: read/write

property_declaration_handler = "http://xml.org/sax/properties/declaration-handler"
# data type: xml.sax.sax2lib.DeclHandler
# description: An optional extension handler for DTD-related events other
#              than notations and unparsed entities.
# access: read/write

property_dom_node = "http://xml.org/sax/properties/dom-node"
# data type: org.w3c.dom.Node
# description: When parsing, the current DOM node being visited if this is
#              a DOM iterator; when not parsing, the root DOM node for
#              iteration.
# access: (parsing) read-only; (not parsing) read/write

property_xml_string = "http://xml.org/sax/properties/xml-string"
# data type: String
# description: The literal string of characters that was the source for
#              the current event.
# access: read-only

property_encoding = "http://www.python.org/sax/properties/encoding"
# data type: String
# description: The name of the encoding to assume for input data.
# access: write: set the encoding, e.g. established by a higher-level
#                protocol. May change during parsing (e.g. after
#                processing a META tag)
#         read:  return the current encoding (possibly established through
#                auto-detection.
# initial value: UTF-8
#

property_interning_dict = "http://www.python.org/sax/properties/interning-dict"
# data type: Dictionary
# description: The dictionary used to intern common strings in the document
# access: write: Request that the parser uses a specific dictionary, to
#                allow interning across different documents
#         read:  return the current interning dictionary, or None
#

all_properties = [property_lexical_handler,
                  property_dom_node,
                  property_declaration_handler,
                  property_xml_string,
                  property_encoding,
                  property_interning_dict]


