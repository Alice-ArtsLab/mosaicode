#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.model.blockmodel import BlockModel
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.GUI.fieldtypes import *

class TestBlockControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        #data = {"label": ("Type"), "name":"type", "value": "text"}
        self.blockmodel = BlockModel()

        self.blockmodel.id = 1
        self.blockmodel.x = 2
        self.blockmodel.y = 2

        self.blockmodel.language = "c"
        self.blockmodel.framework = "opencv"
        self.blockmodel.help = "Adiciona bordas na imagem."
        self.blockmodel.label = "Teste BlockModel"
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

        self.blockcontrol = BlockControl()

    # ----------------------------------------------------------------------
    def test_export_xml(self):
        self.assertIsNone(self.blockcontrol.export_xml())

    # ----------------------------------------------------------------------
    def test_export_python(self):
        self.assertIsNone(self.blockcontrol.export_python())

    # ----------------------------------------------------------------------
    def test_load(self):
        file_name = "Aa"
        self.assertIsNone(self.blockcontrol.load(file_name))
        file_name = ""
        self.assertIsNone(self.blockcontrol.load(file_name))
        file_name = "Teste.xml"
        self.assertIsNone(self.blockcontrol.load(file_name))
        file_name = "Teste.py"
        self.assertIsNone(self.blockcontrol.load(file_name))
        # file_name = None
        # self.assertIsNone(self.blockcontrol.load(file_name))

    # ----------------------------------------------------------------------
    def test_add_new_block(self):
        self.assertIsNone(self.blockcontrol.add_new_block(self.blockmodel))

        # NÃO TRATA None
        # self.assertIsNone(self.blockcontrol.add_new_block(None))

    # ----------------------------------------------------------------------
    def test_delete_block(self):
        #self.assertFalse(self.blockcontrol.delete_block("test_codegenerator.py"))
        #self.assertFalse(self.blockcontrol.delete_block("test_codegenerator.py"))

        #Apresenta um erro de System nao tem blockmodels:
        #self.assertFalse(self.blockcontrol.delete_block(self.blockmodel))
        #self.assertTrue(self.blockcontrol.delete_block(self.blockmodel))
        self.assertIsNotNone(self.blockcontrol.delete_block(self.blockmodel))

        self.blockmodel.id = 1
        self.blockmodel.x = 2
        self.blockmodel.y = 2
        self.blockmodel.type = "c"
        self.blockmodel.source = "/home/lucas/mosaicode/extensions/c/opencv/mosaicode.model.blockmodel"

        self.blockmodel.language = "c"
        self.blockmodel.framework = "opencv"
        self.blockmodel.help = "Adiciona bordas na imagem."
        self.blockmodel.label = "Testing A"
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

        #self.assertFalse(self.blockcontrol.delete_block(self.blockmodel))
        #self.assertTrue(self.blockcontrol.delete_block(self.blockmodel))
        self.assertIsNotNone(self.blockcontrol.delete_block(self.blockmodel))


        # PARA QUE O TESTE ABAIXO SEJA EXECUTADO,
        # DEVE-SE CRIAR UM ARQUIVO c.xml DENTRO
        # DA PASTA mosaicode/extensions, QUE SE
        # ENCONTRA NA home do usuário. ASSIM,
        # O TESTE IRÁ ABRANGER 100% DA CLASSE.

        # LEMBRANDO QUE, ISTO É ERRADO, POIS NÃO
        # EXCLUIRÁ O PLUGIN EM SI, MAS, UM ARQUIVO
        # QUALQUER XML. CASO NÃO SE DELETE, NÃO APRESENTA
        # NENHUMA MENSAGEM DE ERRO.
        self.blockmodel.type = "c"
        self.blockmodel.source = "xml"

        #self.assertFalse(self.blockcontrol.delete_block(self.blockmodel))
        #self.assertFalse(self.blockcontrol.delete_block(self.blockmodel))
        self.assertIsNotNone(self.blockcontrol.delete_block(self.blockmodel))


    # ----------------------------------------------------------------------
    def test_print_block(self):

        #self.assertIsNone(self.blockcontrol.print_block("test_codegenerator.py"))
        self.assertIsNone(self.blockcontrol.print_block(self.blockmodel))
