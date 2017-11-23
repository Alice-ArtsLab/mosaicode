#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.control.codegenerator import CodeGenerator
from mosaicode.GUI.diagram import Diagram

from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.codetemplate import CodeTemplate as CodeTemplate



class TestCodeGenerator(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.blockmodel = BlockModel()

        self.blockmodel.id = 1
        self.blockmodel.x = 2
        self.blockmodel.y = 2

        self.blockmodel.language = "c"
        self.blockmodel.framework = "opencv"
        self.blockmodel.help = "Adiciona bordas na imagem."
        self.blockmodel.label = "Add Border"
        self.blockmodel.color = "0:180:210:150"
        self.blockmodel.in_ports = [{"type":"mosaicode_lib_c_opencv.extensions.ports.image",
                          "name":"input_image",
                          "label":"Input Image"},
                         {"type":"mosaicode_lib_c_opencv.extensions.ports.int",
                          "name":"border_size",
                          "label":"Border Size"}
                         ]
        self.blockmodel.out_ports = [{"type":"mosaicode_lib_c_opencv.extensions.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.blockmodel.group = "Experimental"
        self.blockmodel.properties = [{"label": "Color",
                            "name": "color",
                            "type": MOSAICODE_COLOR,
                            "value":"#FF0000"
                            },
                           {"name": "type",
                            "label": "Type",
                            "type": MOSAICODE_COMBO,
                            "value":"IPL_BORDER_CONSTANT",
                            "values": ["IPL_BORDER_CONSTANT",
                                       "IPL_BORDER_REPLICATE",
                                       "IPL_BORDER_REFLECT",
                                       "IPL_BORDER_WRAP"]
                            },
                           {"label": "Border Size",
                            "name": "border_size",
                            "type": MOSAICODE_INT,
                            "value":"50"
                            }
                           ]
        self.blockmodel.codes[0] = \
            "CvScalar get_scalar_color(const char * rgbColor){\n" + \
            "   if (strlen(rgbColor) < 13 || rgbColor[0] != '#')\n" + \
            "       return cvScalar(0,0,0,0);\n" + \
            "   char r[4], g[4], b[4];\n" + \
            "   strncpy(r, rgbColor+1, 4);\n" + \
            "   strncpy(g, rgbColor+5, 4);\n" + \
            "   strncpy(b, rgbColor+9, 4);\n" + \
            "\n" + \
            "   int ri, gi, bi = 0;\n" + \
            "   ri = (int)strtol(r, NULL, 16);\n" + \
            "   gi = (int)strtol(g, NULL, 16);\n" + \
            "   bi = (int)strtol(b, NULL, 16);\n" + \
            "\n" + \
            "   ri /= 257;\n" + \
            "   gi /= 257;\n" + \
            "   bi /= 257;\n" + \
            "   \n" + \
            "   return cvScalar(bi, gi, ri, 0);\n" + \
            "}\n"
        self.blockmodel.codes[1] = \
            "IplImage * block$id$_img_i0 = NULL;\n" + \
            "int block$id$_int_i1 = $prop[border_size]$;\n" + \
            "IplImage * block$id$_img_o0 = NULL;\n"
        self.blockmodel.codes[2] = \
            'if(block$id$_img_i0){\n' + \
            '\tCvSize size$id$ = cvSize(block$id$_img_i0->width +' + \
            ' block$id$_int_i1 * 2, block$id$_img_i0->height' + \
            ' + block$id$_int_i1 * 2);\n' + \
            '\tblock$id$_img_o0 = cvCreateImage(size$id$,' + \
            ' block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            '\tCvPoint point$id$ = cvPoint' + \
            '(block$id$_int_i1, block$id$_int_i1);\n' + \
            '\tCvScalar color = get_scalar_color("$prop[color]$");\n' + \
            '\tcvCopyMakeBorder(block$id$_img_i0, block$id$_img_o0,' + \
            ' point$id$, $prop[type]$, color);\n' + \
            '}\n'


        win = MainWindow()
        self.diagram = Diagram(win)
        self.codetemplate = CodeTemplate()
        #block = Block(diagram, blockmodel)
        #diagram.language = None
        self.code_generator = CodeGenerator(None, None)
        self.diagram.language = None
        self.code_generator = CodeGenerator(self.diagram, None)
        self.diagram.language = ""
        self.code_generator = CodeGenerator(self.diagram, None)
        self.code_generator = CodeGenerator(self.diagram, self.codetemplate)


    # ----------------------------------------------------------------------
    #def test_replace_wildcards(self):
    #    self.code_generator.replace_wildcards("Teste")

    # ----------------------------------------------------------------------
    def test_get_dir_name(self):
        self.assertIsNotNone(self.code_generator.get_dir_name())
        #self.code_generator.get_dir_name()

    # ----------------------------------------------------------------------
    def test_get_filename(self):
        #from mosaicode.system import System as System
        #print "Ad: " + System.properties.default_directory
        self.assertIsNotNone(self.code_generator.get_filename())
        #self.code_generator.get_filename()

    # ----------------------------------------------------------------------
    #def test_change_directory(self):
    #    self.code_generator.change_directory()

    # ----------------------------------------------------------------------
    #def test_sort_blocks(self):
    #    self.code_generator.sort_blocks()

    # ----------------------------------------------------------------------
    #def test_get_max_weight(self):
    #    self.code_generator.get_max_weight()

    # ----------------------------------------------------------------------
    #def test_generate_parts(self):
    #    self.code_generator.generate_parts()

    # ----------------------------------------------------------------------
    def test_replace_key_value(self):

        key = "2"
        value = "3"
        self.assertIsNone(self.code_generator.replace_key_value(self.blockmodel, key, value))

        key = "1"
        value = "1"
        self.assertIsNone(self.code_generator.replace_key_value(self.blockmodel, key, value))

        #self.code_generator.replace_key_value()

    # ----------------------------------------------------------------------
    def test_generate_block_code(self):
        #self.code_generator.generate_block_code()
        self.assertIsNone(self.code_generator.generate_block_code(self.blockmodel))

    # ----------------------------------------------------------------------
    def test_generate_code(self):
        #self.code_generator.generate_code()
        self.assertIsNotNone(self.code_generator.generate_code())

    # ----------------------------------------------------------------------
    def test_save_code(self):
        name = "None"
        code = "None"
        self.assertIsNone(self.code_generator.save_code(name, code))

        name = "None"
        code = None
        self.assertIsNone(self.code_generator.save_code(name, code))

        # ESTE TESTE E NECESSARIO PARA VERIFICAR
        # SE PODE ACEITAR NONE. EXISTE UM if..else
        # COM name E code = None
        #name = None
        #code = None
        #self.assertIsNone(self.code_generator.save_code(name, code))

    # ----------------------------------------------------------------------
    def test_run(self):
        self.code = None
        self.assertIsNone(self.code_generator.run(self.code))

        self.code = CodeTemplate()
        self.assertIsNone(self.code_generator.run(self.code))

        self.code = "Teste()"
        self.assertIsNone(self.code_generator.run(self.code))

    # ----------------------------------------------------------------------
    #def test_compile(self):
    #    self.code_generator.compile()

    # ----------------------------------------------------------------------
    #def test_execute(self):
    #    self.code_generator.execute()
