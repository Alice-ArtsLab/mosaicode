from unittest import TestCase
from mosaicode.control.codegenerator import CodeGenerator
from mosaicode.GUI.diagram import Diagram
#from mosaicode.GUI.block import Block
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.plugin import Plugin
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.codetemplate import CodeTemplate as CodeTemplate



class TestCodeGenerator(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.plugin = Plugin()

        self.plugin.id = 1
        self.plugin.x = 2
        self.plugin.y = 2

        self.plugin.language = "c"
        self.plugin.framework = "opencv"
        self.plugin.help = "Adiciona bordas na imagem."
        self.plugin.label = "Add Border"
        self.plugin.color = "0:180:210:150"
        self.plugin.in_ports = [{"type":"mosaicode_c_opencv.extensions.ports.image",
                          "name":"input_image",
                          "label":"Input Image"},
                         {"type":"mosaicode_c_opencv.extensions.ports.int",
                          "name":"border_size",
                          "label":"Border Size"}
                         ]
        self.plugin.out_ports = [{"type":"mosaicode_c_opencv.extensions.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.plugin.group = "Experimental"
        self.plugin.properties = [{"label": "Color",
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
        self.plugin.codes[0] = \
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
        self.plugin.codes[1] = \
            "IplImage * block$id$_img_i0 = NULL;\n" + \
            "int block$id$_int_i1 = $prop[border_size]$;\n" + \
            "IplImage * block$id$_img_o0 = NULL;\n"
        self.plugin.codes[2] = \
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
        #block = Block(diagram, plugin)
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
        self.assertIsNone(self.code_generator.replace_key_value(self.plugin, key, value))

        key = "1"
        value = "1"
        self.assertIsNone(self.code_generator.replace_key_value(self.plugin, key, value))

        #self.code_generator.replace_key_value()

    # ----------------------------------------------------------------------
    def test_generate_block_code(self):
        #self.code_generator.generate_block_code()
        self.assertIsNone(self.code_generator.generate_block_code(self.plugin))

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
