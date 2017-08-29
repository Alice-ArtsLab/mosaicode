#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.utils.XMLUtils import XMLParser

FILES_INPUT = "/home/lucas/Faculdade/2017-1/Iniciacao/Mosaicode/mosaicode/test/files_for_test/input/"

class TestXMLParser(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        source = None
        fromString = False
        fromTag = False
        self.xml_parser = XMLParser(source, fromString, fromTag)

        source = FILES_INPUT + "And.mscd"
        fromString = False
        fromTag = False
        self.xml_parser = XMLParser(source, fromString, fromTag)

        # source = FILES_INPUT + "And.mscd"
        # fromString = True
        # fromTag = False
        # self.xml_parser = XMLParser(source, fromString, fromTag)
        #
        # source = "TESTE"
        # fromString = True
        # fromTag = False
        # self.xml_parser = XMLParser(source, fromString, fromTag)
        #
        # source = "TESTE"
        # fromString = False
        # fromTag = True
        # self.xml_parser = XMLParser(source, fromString, fromTag)
        #
        # source = "TESTE"
        # fromString = True
        # fromTag = True
        # self.xml_parser = XMLParser(source, fromString, fromTag)

    # ----------------------------------------------------------------------
    def test_getTagAttr(self):
        self.xml_parser.tag = "property"
        self.xml_parser.attr = "key"
        self.assertIsNotNone(self.xml_parser.getTagAttr(self.xml_parser.tag, self.xml_parser.attr))

        #tag = None
        #attr = None
        #self.assertIsNotNone(self.xml_parser.getTagAttr(tag, attr))

    # ----------------------------------------------------------------------
    def test_setTagAttr(self):
        tag = "position"
        attr = "x"
        self.assertIsNone(self.xml_parser.setTagAttr(tag, attr, 10))

    # ----------------------------------------------------------------------
    def test_getAttr(self):
        #tag = "position"
        attr = "position"
        self.assertIsNotNone(self.xml_parser.getAttr(attr))
        #self.assertEqual(10, self.xml_parser.setTagAttr(attr))

    # ----------------------------------------------------------------------
    def test_setAttr(self):
        attr = "to_block"
        self.assertIsNone(self.xml_parser.setAttr(attr, 10))

    # ----------------------------------------------------------------------
    def test_getChildTagAttr(self):
        parent = "block"
        child = "position"
        attr = "x"
        self.assertIsNotNone(self.xml_parser.getChildTagAttr(parent, child, attr))

    # ----------------------------------------------------------------------
    def test_setChildTagAttr(self):
        parent = "block"
        child = "position"
        attr = "x"
        value = 10
        self.assertIsNone(self.xml_parser.setChildTagAttr(parent, child, attr, value))

    # ----------------------------------------------------------------------
    def test_getChildTags(self):
        child = "position"
        self.assertIsNotNone(self.xml_parser.getChildTags(child))
        child = "block"
        self.assertIsNotNone(self.xml_parser.getChildTags(child))

    # ----------------------------------------------------------------------
    def test_addTag(self):
        tagName = "position"
        self.assertIsNotNone(self.xml_parser.addTag(tagName))

    # ----------------------------------------------------------------------
    def test_appendToTag(self):
        tagParent = "position"
        tagChild = "x"
        self.assertIsNotNone(self.xml_parser.appendToTag(tagParent, tagChild))

    # ----------------------------------------------------------------------
    def test_appendToLastTag(self):
        tagParent = "position"
        tagChild = "x"
        self.assertIsNotNone(self.xml_parser.appendToLastTag(tagParent, tagChild))

    # ----------------------------------------------------------------------
    def test_getXML(self):
        self.assertIsNotNone(self.xml_parser.getXML())

    # ----------------------------------------------------------------------
    def test_getTagXML(self):
        tagName = "position"
        tag = self.xml_parser.addTag(tagName)
        self.assertIsNotNone(self.xml_parser.getTagXML(tag))

    # ----------------------------------------------------------------------
    def test_getTag(self):
        tagName = "position"
        tag = self.xml_parser.addTag(tagName)
        self.assertIsNone(self.xml_parser.getTag(tag))
        tag = "ABC"
        self.assertIsNone(self.xml_parser.getTag(tag))
        tag = "position"
        self.assertIsNotNone(self.xml_parser.getTag(tag))

    # ----------------------------------------------------------------------
    def test_getTagChild(self):
        parent = "block"
        child = "position"
        self.assertIsNotNone(self.xml_parser.getTagChild(parent, child))

    # ----------------------------------------------------------------------
    def test_getTagContent(self):
        self.assertIsNotNone(self.xml_parser.getTagContent())

    # ----------------------------------------------------------------------
    def test_getTagChildren(self):
        self.assertIsNotNone(self.xml_parser.getTagChildren())

    # ----------------------------------------------------------------------
    def test_getText(self):
        self.assertIsNotNone(self.xml_parser.getText())

    # ----------------------------------------------------------------------
    def test_prettify(self):
        self.assertIsNotNone(self.xml_parser.prettify())
