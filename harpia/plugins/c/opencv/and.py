#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the And class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class And(OpenCVPlugin):
    """
    This class contains methods related the And class.
    """
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
        self.label = "And"
        self.color = "10:180:10:150"
        self.in_ports = [{"type":"HRP_IMAGE",
                          "name":"first_image",
                          "label":"First Image"},
                         {"type":"HRP_IMAGE",
                          "name":"second_image",
                          "label":"Second Image"}
                         ]
        self.out_ports = [{"type":"HRP_IMAGE",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Arithmetic and logical operations"

        self.codes[0] = r"""
// And, Xor, Division, subtraction, sum, or,
//multiplication need images with the same size
void adjust_images_size(IplImage * img1, IplImage * img2, IplImage * img3){
    if(img1->width != img2->width || img1->height != img2->height){
    int minW,minH;
    if(img1->width > img2->width)
        minW = img2->width;
    else
        minW = img1->width;

    if(img1->height > img2->height)
        minH = img2->height;
    else
        minH = img1->height;

    cvSetImageROI(img2, cvRect( 0, 0, minW, minH ));
    cvSetImageROI(img1, cvRect( 0, 0, minW, minH ));
    cvSetImageROI(img3, cvRect( 0, 0, minW, minH ));
    }
}
"""

        self.codes[1] = "// $id$ - And\n" + \
                    "IplImage * block$id$_img_i0 = NULL;\n" + \
                    "IplImage * block$id$_img_i1 = NULL;\n" + \
                    "IplImage * block$id$_img_o0 = NULL;\n"

        self.codes[2] = \
            '\nif(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tadjust_images_size(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0);\n' + \
            '\tcvAnd(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0,0);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'

        self.codes[3] = "cvReleaseImage(&block$id$_img_i0);\n" + \
                    "cvReleaseImage(&block$id$_img_i1);\n" + \
                    "cvReleaseImage(&block$id$_img_o0);\n"

# -----------------------------------------------------------------------------
