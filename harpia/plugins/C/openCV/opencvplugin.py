#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the OpenCVPlugin class.
"""
from harpia.model.plugin import Plugin


class OpenCVPlugin(Plugin):
    """
    This class contains methods related the OpenCVPlugin class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.language = "C"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        if self.vars != "":
            return self.vars
        value = ""
        count = 0
        for in_type in self.get_in_types():
            if in_type == "HRP_IMAGE":
                value += 'IplImage * block$id$_img_i' + \
                    str(count) + ' = NULL;\n'
            if in_type == "HRP_INT":
                value += 'int block$id$_int_i' + str(count) + ' = 0;\n'
            if in_type == "HRP_RECT":
                value += 'CvRect block$id$_rect_i' + \
                    str(count) + ' = cvRect( 0, 0, 1, 1);\n'
            if in_type == "HRP_POINT":
                value += 'CvPoint block$id$_point_i' + str(count) + ';\n'
            if in_type == "HRP_DOUBLE":
                value += 'double block$id$_double_i' + str(count) + ';\n'
            count += 1

        count = 0
        for out_type in self.get_out_types():
            if out_type == "HRP_IMAGE":
                value += 'IplImage * block$id$_img_o' + \
                    str(count) + ' = NULL;\n'
            if out_type == "HRP_INT":
                value += 'int block$id$_int_o' + str(count) + ' = 0;\n'
            if out_type == "HRP_RECT":
                value += 'CvRect block$id$_rect_o' + \
                    str(count) + ' = cvRect( 0, 0, 1, 1);\n'
            if out_type == "HRP_POINT":
                value += 'CvPoint block$id$_point_o' + \
                    str(count) + ' = cvPoint(0,0);\n'
            if out_type == "HRP_DOUBLE":
                value += 'double block$id$_double_o' + str(count) + ';\n'
            count += 1

        return value

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        if self.dealloc != "":
            return self.dealloc
        value = ""
        count = 0
        for x in self.get_in_types():
            if x == "HRP_IMAGE":
                value += 'cvReleaseImage(&block$id$_img_i' + \
                    str(count) + ');\n'
            count += 1
        count = 0
        for x in self.get_out_types():
            if x == "HRP_IMAGE":
                value += 'cvReleaseImage(&block$id$_img_o' + \
                    str(count) + ');\n'
            count += 1
        return value

    # ----------------------------------------------------------------------
    def get_adjust_images_size(self):
        return r"""
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

# -----------------------------------------------------------------------------
