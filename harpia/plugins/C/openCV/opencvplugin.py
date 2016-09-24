#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from harpia.model.plugin import Plugin

class OpenCVPlugin(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

    # ----------------------------------------------------------------------
    def generate_vars(self):
        value = ""
        for x in self.get_description()["InTypes"]:
            if self.get_description()["InTypes"][x] == "HRP_IMAGE":
                value += 'IplImage * block$id$_img_i' + str(x) + ' = NULL;\n'
            if self.get_description()["InTypes"][x] == "HRP_INT":
                value += 'int block$id$_int_i' + str(x) + ' = 0;\n'
            if self.get_description()["InTypes"][x] == "HRP_RECT":
                value += 'CvRect block$id$_rect_i' + str(x) + ' = cvRect( 0, 0, 1, 1);\n'
            if self.get_description()["InTypes"][x] == "HRP_POINT":
                value += 'CvPoint block$id$_point_i' + str(x) + ';\n'
            if self.get_description()["InTypes"][x] == "HRP_DOUBLE":
                value += 'double block$id$_double_i' + str(x) + ';\n'

        for x in self.get_description()["OutTypes"]:
            if self.get_description()["OutTypes"][x] == "HRP_IMAGE":
                value += 'IplImage * block$id$_img_o' + str(x) + ' = NULL;\n'
            if self.get_description()["OutTypes"][x] == "HRP_INT":
                value += 'int block$id$_int_o' + str(x) + ' = 0;\n'
            if self.get_description()["OutTypes"][x] == "HRP_RECT":
                value += 'CvRect block$id$_rect_o' + str(x) + ' = cvRect( 0, 0, 1, 1);\n'
            if self.get_description()["OutTypes"][x] == "HRP_POINT":
                value += 'CvPoint block$id$_point_o' + str(x) + ' = cvPoint(0,0);\n'
            if self.get_description()["OutTypes"][x] == "HRP_DOUBLE":
                value += 'double block$id$_double_o' + str(x) + ';\n'

        return value

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        value = ""
        for x in self.get_description()["InTypes"]:
            if self.get_description()["InTypes"][x] == "HRP_IMAGE":
                value += 'cvReleaseImage(&block$id$_img_i' + str(x) + ');\n'
        for x in self.get_description()["OutTypes"]:
            if self.get_description()["OutTypes"][x] == "HRP_IMAGE":
                value += 'cvReleaseImage(&block$id$_img_o' + str(x) + ');\n'
        return value

    # ----------------------------------------------------------------------
    def get_adjust_images_size(self):
        return r"""
// And, Xor, Division, subtraction, sum, or, multiplication need images with the same size
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

# ------------------------------------------------------------------------------
