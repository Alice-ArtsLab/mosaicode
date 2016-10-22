#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class And(OpenCVPlugin):

    # ------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Permite a operação lógica 'E' entre as duas entradas." + \
            " Para esse bloco há duas possibilidades." + \
            "Primeira: Executa a operação entre" + \
            " duas imagens ponto a ponto." + \
            "Segunda: Executa a operação entre um " + \
            "valor constante e cada ponto da imagem."
        self.label = "And
        self.icon = "images/and.png"
        self.color = "10:180:10:150"
        self.in_types = ["HRP_IMAGE", "HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Arithmetic and logical operations"

        # --------------------c/OpneCV code----------------------------
        self.function_call = \
            '\nif(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tadjust_images_size(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0);\n' + \
            '\tcvAnd(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0,0);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
