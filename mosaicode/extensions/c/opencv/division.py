#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Division class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class Division(Plugin):
    """
    This class contains methods related the Division class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        # Appearance
        self.help = "Realiza a divisão de duas imagens."
        self.label = "Division"
        self.color = "180:10:10:150"
        self.in_ports = [{"type":"mosaicode.extensions.c.ports.image",
                          "name":"first_image",
                          "label":"First Image"},
                         {"type":"mosaicode.extensions.c.ports.image",
                          "name":"first_image",
                          "label":"First Image"}
                         ]
        self.out_ports = [{"type":"mosaicode.extensions.c.ports.image",
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

        self.codes[2] = \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'adjust_images_size(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0);\n' + \
            'cvDiv(block$id$_img_i0, block$id$_img_i1, ' + \
            'block$id$_img_o0,1);\n' + \
            'cvResetImageROI(block$id$_img_o0);\n}\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
