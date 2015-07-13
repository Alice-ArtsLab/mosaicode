# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2004 - 2006 Christian Silvano (christian.silvano@gmail.com), Mathias Erdtmann (erdtmann@gmail.com), S2i (www.s2i.das.ufsc.br)
#            2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
#----------------------------------------------------------------------

################################WARNING!!###########################################
#                      DO NOT MANUALLY EDIT THIS FILE                              #
# LET THE MODIFICATIONS BE INSERTED BY THE TOOLS PROVIDED WITH HARPIA SYSTEM       #
####################################################################################

#############################INCLUDES AND DECLARATIONS##############################
import os
import gtk
#from popen2 import Popen4
from amara import binderytools

# Bug fix -  Schiavoni
import subprocess

#i18n
import gettext
APP='harpia'
DIR='/usr/local/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


import s2idirectory

arguments = []
images = []
functionCalls = []
deallocations = []
outDeallocations = []
blockList = []

ErrorLog = 'ErrorLog'

if os.name=="nt":
    tmpDir = os.path.join(os.path.expanduser ("~"), "tmp\\")
    if not( os.path.exists(tmpDir) ):
            os.makedirs(tmpDir, mode=0700)
else:
    tmpDir = "/tmp/" 

def cleanGenerator():
    global arguments,images,functionCalls,deallocations,outDeallocations,blockList
    arguments = []
    images = []
    functionCalls = []
    deallocations = []
    outDeallocations = []
    blockList = []
    
# Global variable to indicate overall behavior of the code generator

g_bLive = False #default eh live!!

g_ShowCount = 0

g_bCameras = []
g_bVideo = [] #default eh live!!
g_bSaveVideo = []

g_bFrameRate = 0.1

g_sCaptureLive = '0'
g_sVideoFilename = ''
#g_flagFrame = 1

usesFindSquares = 0
usesFindColor = 0

####################################################################################

######################### input images with different sizes must be treated ########

def	inputSizeComply(nInputs, currentBlockN):
	if nInputs == 2:
		outPutCode = 'if(block' + str(currentBlockN) + '_img_i1->width != block' + str(currentBlockN) + '_img_i2->width || ' + \
									'block' + str(currentBlockN) + '_img_i1->height != block' + str(currentBlockN) + '_img_i2->height)\n{\n' + \
									'	int minW,minH;\n' + \
									'	if(block' + str(currentBlockN) + '_img_i1->width > block' + str(currentBlockN) + '_img_i2->width)\n' + \
									'		minW = block' + str(currentBlockN) + '_img_i2->width;\n' + \
									'	else \n' + \
									'		minW = block' + str(currentBlockN) + '_img_i1->width;\n\n' + \
									'	if(block' + str(currentBlockN) + '_img_i1->height > block' + str(currentBlockN) + '_img_i2->height)\n' + \
									'		minH = block' + str(currentBlockN) + '_img_i2->height;\n' + \
									'	else \n' + \
									'		minH = block' + str(currentBlockN) + '_img_i1->height;\n\n' + \
									'	cvSetImageROI(block' + str(currentBlockN) + '_img_i2, cvRect( 0, 0, minW, minH ));\n' + \
									'	cvSetImageROI(block' + str(currentBlockN) + '_img_i1, cvRect( 0, 0, minW, minH ));\n' + \
									'	cvSetImageROI(block' + str(currentBlockN) + '_img_o1, cvRect( 0, 0, minW, minH ));\n' + \
									'}\n'
		return(outPutCode)
	else:
		return("//Image Sizes match\n")


#####################################CLASSES############################
##################### connection ###########################
class connection:
    sourceOutput = '00'
    destinationNumber = '00'
    destinationInput = '00'
    connType = " "

############################################################
##################### block templates ######################
class blockTemplate:
    blockType = 'NA'
    blockNumber = 'NA'
    imagesIO = ''
    functionArguments = ''
    outputCopy = ''
    xmlResult = ''
    dealloc = ''
    outDealloc = ''
    properties = []
    myConnections = []
    outputsToSave = []
    weight = 1
    outTypes = []

		
###########################################################################

######################################################3
#### Added by cpscotti. blockTemplate needs its outputTypes even "before" its code.. here it is
    def getBlockOutputTypes(self):
			try:
				self.outTypes = s2idirectory.block[int(self.blockType)]["OutTypes"]
			except:
				self.outTypes = "HRP_IMAGE","HRP_IMAGE","HRP_IMAGE","HRP_IMAGE"

############################### processors #################################
# THIS CODE IS TO CREATE THE C LINES FROM THE XML PARSING                  #
############################################################################
    def blockCodeWriter(self):
############################################################################
        if self.blockType == '00': #ACQUISITION BLOCK
            for propIter in self.properties:
                if propIter[0] == 'type':
                    flag = propIter[1]
                    if ( (flag == 'live') or (flag == 'video')): # (propIter[0] == 'live' and (flag<>'file') and (flag<>'camera')):
                        global g_bLive
                        g_bLive = True
                if ( (propIter[0] == 'filename') and (flag == 'file') ):
                    argFilename = propIter[1]
                if ( ( propIter[0] == 'size') and (flag == 'newimage') ):
                    size = propIter[1]
                    Width = size[ :size.find('x')]
                    Height = size[size.find('x')+1: ]
                if (propIter[0] == 'camera' and flag == 'live'):#(flag<>'file') and (flag<>'newimage') and (flag<>'live')):
                    global g_bCameras
                    tmpPack = [] #contendo [ blockNumber , camNum ]
                    tmpPack.append(self.blockNumber)
                    tmpPack.append(propIter[1])
                    g_bCameras.append(tmpPack)
                if (propIter[0] == 'camera' and flag == 'camera'):#(flag<>'file') and (flag<>'newimage') and (flag<>'live')):
                    captureCamNumber = propIter[1]
                if(propIter[0] == 'video_name' and flag == 'video'):
                    global g_bVideo
                    tmpPack = []
                    tmpPack.append(self.blockNumber)
                    tmpPack.append(propIter[1])
                    g_bVideo.append(tmpPack)
                if propIter[0] == 'frameRate':
                    global g_bFrameRate
                    if float(propIter[1]) > g_bFrameRate:
                    	g_bFrameRate = float(propIter[1])
            self.imagesIO = \
                 'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            if flag == 'camera':
                #global g_bCameras #pegaremos o segundo elemento da ultima lista anexada a a lista g_bCameras (isso eh o numero da ultima camera)
                self.functionCall = \
                    'CvCapture* block' + self.blockNumber + '_capture = NULL; \n' + \
                    'IplImage* block' + self.blockNumber + '_frame = NULL; \n' + \
                    'block' + self.blockNumber + '_capture = cvCaptureFromCAM(' + captureCamNumber + '); \n' + \
                    'if( !cvGrabFrame( block' + self.blockNumber + '_capture ) \n ) { printf("Cannot Grab Image from camera '+ captureCamNumber +'"); }' + \
                    'block' + self.blockNumber + '_frame = cvRetrieveFrame( block' + self.blockNumber + '_capture ); ' + \
                    'if( !cvGrabFrame( block' + self.blockNumber + '_capture ) \n ) { printf("Cannot Grab Image from camera '+ captureCamNumber +'"); }' + \
                    'block' + self.blockNumber + '_frame = cvRetrieveFrame( block' + self.blockNumber + '_capture ); ' + \
                    'if( !cvGrabFrame( block' + self.blockNumber + '_capture ) \n ) { printf("Cannot Grab Image from camera '+ captureCamNumber +'"); }' + \
                    'block' + self.blockNumber + '_frame = cvRetrieveFrame( block' + self.blockNumber + '_capture ); ' + \
                    'block' + self.blockNumber + '_img_o1 = cvCloneImage( block' + self.blockNumber + '_frame );\n'
            if flag == 'video':
                self.functionCall = '// Video Mode \n' + 'block' + self.blockNumber + '_img_o1 = cvCloneImage( block' + self.blockNumber + '_frame );\n'
            if flag == 'file':
                self.functionArguments = \
                 'char block' + self.blockNumber + '_arg_Filename[] = "' + argFilename + '";\n'
                self.functionCall = \
                    'block' + self.blockNumber + '_img_o1 = cvLoadImage(block' + self.blockNumber + '_arg_Filename,-1);\n'
            if flag == 'live':
                self.functionCall = '// Live Mode \n' + 'block' + self.blockNumber + '_img_o1 = cvCloneImage( block' + self.blockNumber + '_frame );\n'
            if flag == 'newimage':
                self.functionCall = \
                     'CvSize size = cvSize(' + Width +','+ Height +');\n' + \
                     'block' + self.blockNumber + '_img_o1 = cvCreateImage(size,IPL_DEPTH_8U,3);\n' + \
                     'cvSetZero(block' + self.blockNumber + '_img_o1);\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n'
#############################################################################
        elif self.blockType == '06': # COLORSPACE CONVERSION
            channels = '3'
            for propIter in self.properties:
                if propIter[0] == 'type':
                    if propIter[1] == 'RGB -> GRAY':
                        code = 'CV_RGB2GRAY'
                        channels = '1';
                    elif propIter[1] == 'RGB -> YCrCb':
                        code = 'CV_RGB2YCrCb'
                    elif propIter[1] == 'YCrCb -> RGB':
                        code = 'CV_YCrCb2RGB'
                    elif propIter[1] == 'RGB -> HSV':
                        code = 'CV_RGB2HSV'
                    elif propIter[1] == 'HSV -> RGB':
                        code = 'CV_HSV2RGB'
                    elif propIter[1] == 'RGB -> HLS':
                        code = 'CV_RGB2HLS'
                    elif propIter[1] == 'HLS -> RGB':
                        code = 'CV_HLS2RGB'
                    elif propIter[1] == 'RGB -> CIE.XYZ':
                        code = 'CV_RGB2XYZ'
                    elif propIter[1] == 'CIE.XYZ -> RGB':
                        code = 'CV_XYZ2RGB'
                    elif propIter[1] == 'RGB -> CIE.LAB':
                        code = 'CV_RGB2Lab'
                    elif propIter[1] == 'CIE.LAB -> RGB':
                        code = 'CV_Lab2RGB'
                    elif propIter[1] == 'RGB -> CIE.LUV':
                        code = 'CV_RGB2Luv'
                    elif propIter[1] == 'CIE.LUV -> RGB':
                        code = 'CV_Luv2RGB'
                # Standard
                #else:
                   # code = 'CV_RGB2GRAY'
                   # channels = '1'
            self.imagesIO = \
                 'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                 'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                 'IplImage * block' + self.blockNumber + '_img_t = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n'+ \
                               'block' + self.blockNumber + '_img_t = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth,' + channels +');\n'+ \
                              'cvCvtColor(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_t ,' + code +' );}\n' + \
                              'if ( '+code+ ' == ' + "CV_RGB2GRAY" + ')\n' + \
                              '{    cvMerge(block' + self.blockNumber + '_img_t ,block' + self.blockNumber + '_img_t ,block'+ self.blockNumber + '_img_t ,NULL ,block'+ self.blockNumber + '_img_o1);\n }\n' + \
                              'else\n' + '{ block'+ self.blockNumber + '_img_o1 = cvCloneImage(block' + self.blockNumber + '_img_t);\n}'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_t);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n'
                            
#############################################################################
        elif self.blockType == '07': # COMPOSICAO RGB
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i3 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t3 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, block' + \
                               self.blockNumber + '_img_i1->nChannels);\n'+\
                               'block' + self.blockNumber + '_img_t1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, 1);\n'+\
                               'block' + self.blockNumber + '_img_t2 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, 1);\n'+\
                               'block' + self.blockNumber + '_img_t3 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, 1);\n'+\
                               'cvSplit(block' + self.blockNumber + '_img_i1 ,block' + self.blockNumber + '_img_t1  ,NULL, NULL , NULL);\n' + \
                               'cvSplit(block' + self.blockNumber + '_img_i2 ,NULL ,block' + self.blockNumber + '_img_t2, NULL, NULL);\n' + \
                               'cvSplit(block' + self.blockNumber + '_img_i3 ,NULL ,NULL, block' + self.blockNumber + '_img_t3 , NULL);\n' + \
                               'cvMerge(block' + self.blockNumber + '_img_t3 ,block' + self.blockNumber + '_img_t2 ,block'+ self.blockNumber + '_img_t1 , NULL, block'+ \
                               self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_t1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t2);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t3);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i3);\n'
#############################################################################
        elif self.blockType == '08': # DECOMPOSICAO RGB
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t3 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o3 = NULL;\n'
            self.functionCall = \
                                '\nif(block' + self.blockNumber + '_img_i1){\n' + 'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, block' + \
                               self.blockNumber + '_img_i1->nChannels);\n'+\
                               'block' + self.blockNumber + '_img_o2 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, block' + \
                               self.blockNumber + '_img_i1->nChannels);\n'+\
                               'block' + self.blockNumber + '_img_o3 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, block' + \
                               self.blockNumber + '_img_i1->nChannels);\n' + \
                               'block' + self.blockNumber + '_img_t1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, 1);\n' + \
                               'block' + self.blockNumber + '_img_t2 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, 1);\n' +\
                               'block' + self.blockNumber + '_img_t3 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth, 1);\n' + \
                               'cvSplit(block' + self.blockNumber + '_img_i1 ,block' + self.blockNumber + '_img_t3 ,block' + self.blockNumber + '_img_t2 ,block' + self.blockNumber + '_img_t1 , NULL);\n' + \
                               'cvMerge(block' + self.blockNumber + '_img_t1 ,block' + self.blockNumber + '_img_t1 , block' + self.blockNumber + '_img_t1 , NULL, block' + \
                               self.blockNumber + '_img_o1);\n' + \
                               'cvMerge(block' + self.blockNumber + '_img_t2 ,block' + self.blockNumber + '_img_t2, block' + self.blockNumber + '_img_t2, NULL, block'+ \
                               self.blockNumber + '_img_o2);\n' + \
                               'cvMerge(block' + self.blockNumber + '_img_t3 ,block' + self.blockNumber + '_img_t3, block' + self.blockNumber + '_img_t3, NULL, block'+ \
                               self.blockNumber + '_img_o3);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_t1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t2);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t3);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_o2);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_o3);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
#############################################################################
        elif self.blockType == '09': # FILL BLOCK
            for propIter in self.properties:
                if propIter[0] == 'red':
                    red = propIter[1]
                elif propIter[0] == 'green':
                    green = propIter[1]
                elif propIter[0] == 'blue':
                    blue = propIter[1]
            self.imagesIO = \
                 'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                 'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = \
                 '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                 'block' + self.blockNumber + '_img_o1 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
                 '\nCvScalar color = cvScalar('+blue +','+ green +','+ red+',0);\n' + \
                 '\ncvSet(block' + self.blockNumber + '_img_o1,color,NULL);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
#############################################################################
        elif self.blockType == '14': # FILL RECT BLOCK
            for propIter in self.properties:
                if propIter[0] == 'red':
                    red = propIter[1]
                elif propIter[0] == 'green':
                    green = propIter[1]
                elif propIter[0] == 'blue':
                    blue = propIter[1]
            self.imagesIO = \
                 'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                 'CvRect block' + self.blockNumber + '_rect_i2;\n' + \
                 'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = \
                 '\nif(block' + self.blockNumber + '_img_i1)\n{\n' + \
                 '\tblock' + self.blockNumber + '_img_o1 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
                 '\tcvSetImageROI(block' + self.blockNumber + '_img_o1 , block' + self.blockNumber + '_rect_i2);\n' + \
                 '\tCvScalar color = cvScalar('+blue +','+ green +','+ red+',0);\n' + \
                 '\tcvSet(block' + self.blockNumber + '_img_o1,color,NULL);\n' + \
                 '\tcvResetImageROI(block' + self.blockNumber + '_img_o1);\n' + \
                 '}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
#############################################################################
        elif self.blockType == '10': #COMMENT
            for propIter in self.properties:
                if propIter[0] == 'comment':
                    comment = propIter[1]
            self.functionCall = '/*'+comment+'*/ \n'
#############################################################################
        elif self.blockType == '120': # THRESHOLD BLOCK
            for propIter in self.properties:
                if propIter[0] == 'threshold':
                    thresholdValue = propIter[1]
                elif propIter[0] == 'maxValue':
                    maxValue = propIter[1]
                elif propIter[0] == 'thresholdType':
                    thresholdType = propIter[1]
            
            self.imagesIO = \
                 'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                 'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionArguments = \
                 'int block' + self.blockNumber + '_arg_threshold = ' + thresholdValue + ';\n' + \
                 'int block' + self.blockNumber + '_arg_maxValue = ' + maxValue + ';\n' + \
                 'int block' + self.blockNumber + '_arg_thresholdType = ' + thresholdType + ';\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                 'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                 '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                 '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                 '\ncvThreshold(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + \
                 '_img_o1,block' + self.blockNumber + '_arg_threshold,block' + self.blockNumber + \
                 '_arg_maxValue,block' + self.blockNumber + '_arg_thresholdType);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
#############################################################################
        elif self.blockType == '80':# SOBEL
            for propIter in self.properties:
                if propIter[0] == 'xorder':
                    xOrderValue = propIter[1]
                if propIter[0] == 'yorder':
                    yOrderValue = propIter[1]
                if propIter[0] == 'masksize':
                    masksizeValue = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_32F,block'+ \
				    self.blockNumber + '_img_i1->nChannels);\n'+\
                              'cvSobel(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_o1 ,' + xOrderValue +','+ yOrderValue +','+masksizeValue+' );}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t);\n'
#############################################################################
        elif self.blockType == '81':# LAPLACE
            for propIter in self.properties:
                if propIter[0] == 'masksize':
                    masksizeValue = propIter[1]
		else:
		    masksizeValue = '3'
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_32F,block'+ \
				    self.blockNumber + '_img_i1->nChannels);\n'+\
                              'cvLaplace(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_o1 ,' + masksizeValue+' );}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t);\n'
#############################################################################
        elif self.blockType == '82':# SUAVIZADOR
            for propIter in self.properties:
                if propIter[0] == 'type':
                    typeValue = propIter[1]
                elif propIter[0] == 'param1':
                    param1Value = propIter[1]
                elif propIter[0] == 'param2':
                    param2Value = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_t = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber + '_img_i1->depth,block'+ \
				    self.blockNumber + '_img_i1->nChannels);\n'+\
                              'cvSmooth(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_o1 ,' + typeValue + ',' + param1Value + ',' + param2Value +',0,0);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t);\n'
 ############################################################################
        elif self.blockType == '83': # CANNY BLOCK
            for propIter in self.properties:
                if propIter[0] == 'threshold2':
                    threshold2Value = propIter[1]
                elif propIter[0] == 'apertureSize':
                    apertureSizeValue = propIter[1]
                elif propIter[0] == 'threshold1':
                    threshold1Value = propIter[1]
            self.imagesIO = \
                'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\nIplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionArguments = \
                'int block' + self.blockNumber + '_arg_threshold2 = ' + threshold2Value + \
                ';\nint block' + self.blockNumber + '_arg_aperture_size = ' + apertureSizeValue + \
                ';\nint block' + self.blockNumber + '_arg_threshold1 = ' + threshold1Value + ';\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n IplImage * tmpImg' +self.blockNumber+\
                ' = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1),8,1);\n if(block' + self.blockNumber +\
                '_img_i1->nChannels == 3)\n {cvCvtColor(block' + self.blockNumber + '_img_i1,tmpImg' + self.blockNumber +\
                ',CV_RGB2GRAY);}\n else\n{tmpImg' + self.blockNumber + ' = block' + self.blockNumber + \
                '_img_i1 = NULL;}\n cvCanny(tmpImg' + self.blockNumber + ', tmpImg' + self.blockNumber + \
                ', block' + self.blockNumber + '_arg_threshold1, block' + self.blockNumber + \
                '_arg_threshold2, block' + self.blockNumber + '_arg_aperture_size);\n'+ \
                'if(block' + self.blockNumber + '_img_i1->nChannels == 3)\n{cvCvtColor(tmpImg' + self.blockNumber + \
                ', block' + self.blockNumber + '_img_o1,CV_GRAY2RGB);}\nelse\n{cvCopyImage(tmpImg' + self.blockNumber +\
                ', block' + self.blockNumber + '_img_o1);}\ncvReleaseImage(&tmpImg' + self.blockNumber + ');}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
	elif self.blockType == '100': # ERODE BLOCK
            for propIter in self.properties:
                if propIter[0] == 'masksize':
                    maskSizeValue = propIter[1]
                elif propIter[0] == 'iterations':
                    iterationsValue = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\nIplImage * block' + \
                          self.blockNumber + '_img_o1 = NULL;\n'
            self.functionArguments = 'int block' + self.blockNumber + '_arg_iterations = ' + \
                                     iterationsValue + ';\nIplConvKernel * block' + self.blockNumber + \
                                     '_arg_mask = cvCreateStructuringElementEx(' + maskSizeValue[0] + \
                                     ' , ' + maskSizeValue[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width, block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber+\
                              '_img_i1->depth ,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                              '\ncvErode(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + \
                              '_img_o1,block' + self.blockNumber + '_arg_mask,block' + self.blockNumber + \
                              '_arg_iterations);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
	elif self.blockType == '101': # DILATE
            for propIter in self.properties:
                if propIter[0] == 'masksize':
                    maskSizeValue = propIter[1]
                elif propIter[0] == 'iterations':
                    iterationsValue = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                           'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionArguments = 'int block' + self.blockNumber + '_arg_iterations = ' + iterationsValue + \
                                     ';\nIplConvKernel * block' + self.blockNumber + \
                                     '_arg_mask = cvCreateStructuringElementEx(' + maskSizeValue[0] + ' , ' + \
                                     maskSizeValue[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width, block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber +\
                              '_img_i1->depth ,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                              '\ncvDilate(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + \
                              '_img_o1,block' + self.blockNumber + '_arg_mask,block' + self.blockNumber + \
                              '_arg_iterations);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
	elif self.blockType == '102': #OPENING
            for propIter in self.properties:
                if propIter[0] == 'masksize':
                    maskSizeValue = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                           'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionArguments = 'IplConvKernel * block' + self.blockNumber + \
                                     '_arg_mask = cvCreateStructuringElementEx(' + maskSizeValue[0] + ' , ' + \
                                     maskSizeValue[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'IplImage * block' + self.blockNumber + '_auxImg;' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width, block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber +\
                              '_img_i1->depth ,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                              '\nblock' + self.blockNumber + '_auxImg = cvCreateImage(cvSize(block' + self.blockNumber +\
                              '_img_i1->width, block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber +\
                              '_img_i1->depth ,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                              'cvMorphologyEx(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o1,NULL,' + \
                              'block'  + self.blockNumber + '_arg_mask, CV_MOP_OPEN, 1);\n}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseStructuringElement(&block' + self.blockNumber + '_arg_mask);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
	elif self.blockType == '103': #CLOSING
            for propIter in self.properties:
                if propIter[0] == 'masksize':
                    maskSizeValue = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                           'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionArguments = 'IplConvKernel * block' + self.blockNumber + \
                                     '_arg_mask = cvCreateStructuringElementEx(' + maskSizeValue[0] + ' , ' + \
                                     maskSizeValue[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'IplImage * block' + self.blockNumber + '_auxImg;' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width, block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber +\
                              '_img_i1->depth ,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                              '\nblock' + self.blockNumber + '_auxImg = cvCreateImage(cvSize(block' + self.blockNumber +\
                              '_img_i1->width, block' + self.blockNumber + '_img_i1->height), block' + self.blockNumber +\
                              '_img_i1->depth ,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
                              'cvMorphologyEx(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o1,NULL,' + \
                              'block'  + self.blockNumber + '_arg_mask, CV_MOP_CLOSE, 1);\n}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseStructuringElement(&block' + self.blockNumber + '_arg_mask);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
	elif self.blockType == '01': # SAVE
            for propIter in self.properties:
                if propIter[0] == 'filename':
                    saveFilename = os.path.expanduser(propIter[1])
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                           'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = \
                              'block' + self.blockNumber + '_img_o1 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
                               '\nif(block' + self.blockNumber + '_img_i1)\n' + \
                              'cvSaveImage("' + saveFilename + '" ,block' +self.blockNumber+'_img_i1);\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
	elif self.blockType == '02': # SHOW
            global g_ShowCount
            g_ShowCount += 1
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            if(not g_bLive):
                self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
			      ' block' + self.blockNumber + '_img_o1 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
                                'cvSaveImage("block' + self.blockNumber + '_OUT.png" ,block' +self.blockNumber+'_img_i1);}\n'
            else:
                self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                  ' block' + self.blockNumber + '_img_o1 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
                                'cvNamedWindow("block' + self.blockNumber + '_img_o1",CV_WINDOW_AUTOSIZE );\n cvShowImage("block' + self.blockNumber + '_img_o1",block' + self.blockNumber + '_img_i1);} \n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
############################################################################
        elif self.blockType == '20': #SUM
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvAdd(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,0);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
############################################################################
        elif self.blockType == '21': #SUBTRACTION
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvSub(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,0);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
############################################################################
        elif self.blockType == '22': #MULTIPLICATION
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvMul(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,1);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
############################################################################
        elif self.blockType == '23': #DIVISION
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvDiv(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,1);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
#############################################################################
        elif self.blockType == '60':#POW
            for propIter in self.properties:
                if propIter[0] == 'exponent':
                    exponent = propIter[1]
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\ncvPow(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_o1,' + str(exponent) +');}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
 ############################################################################
        elif self.blockType == '61':#Exp
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
						  						'IplImage * block' + self.blockNumber + '_img_t = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_t = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_32F,block'+ \
				    self.blockNumber + '_img_i1->nChannels);\n'+\
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
				'cvConvertScale(block'+ self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_t,(1/255.0),0);\n' + \
			   	'cvExp(block' + self.blockNumber + '_img_t, block' + self.blockNumber + '_img_t);\n' + \
			    	'cvConvertScale(block'+ self.blockNumber + '_img_t,block' + self.blockNumber + '_img_o1,(double)93.8092,0);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t);\n'
 ############################################################################
        elif self.blockType == '62':#Log
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
						  						'IplImage * block' + self.blockNumber + '_img_t = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_t = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_32F,block'+ \
            self.blockNumber + '_img_i1->nChannels);\n'+\
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
				'cvConvertScale(block'+ self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_t,(1/93.8092),0);\n' + \
			   	'cvLog(block' + self.blockNumber + '_img_t, block' + self.blockNumber + '_img_t);\n' + \
			    	'cvConvertScale(block'+ self.blockNumber + '_img_t,block' + self.blockNumber + '_img_o1,255.0,0);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_t);\n'
#############################################################################
        elif self.blockType == '40': #NOT
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\ncvNot(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
#############################################################################
        elif self.blockType == '41': #AND
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' +\
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvAnd(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,0);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
#############################################################################
        elif self.blockType == '42': #OR
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvOr(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,0);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
#############################################################################
        elif self.blockType == '43': #XOR
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                               'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                               '_img_i1->width,block' + self.blockNumber + '_img_i1->height),block' + self.blockNumber + \
                               '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															 inputSizeComply(2,self.blockNumber) + 'cvXor(block' + \
                               self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_i2, block' + \
                               self.blockNumber + '_img_o1,0);\n cvResetImageROI(block' + self.blockNumber + '_img_o1);}\n'
            self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                           'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n'
#############################################################################
        elif self.blockType == '601': #EXEC_CMD, check (0,0), not null.. change this.. cmd = echo auehueah, change this
					cmdString = 'echo no properties'
					enIsntZero = False
					for propIter in self.properties:
						if propIter[0] == 'cmdString':
							cmdString = propIter[1]
						if propIter[0] == 'enIsntZero':
							enIsntZero = (propIter[1] == "True")
					cmdString = cmdString.replace(r"'",r"\'")
					cmdString = cmdString.replace(r'"',r'\"')
					self.imagesIO = \
                          'double block' + self.blockNumber + '_double_i1;\n' + \
                          'double block' + self.blockNumber + '_double_o1;\n'
					self.functionCall = '\nif('
					if enIsntZero:
						self.functionCall += 'block' + self.blockNumber + '_double_i1 > 0.0){\n'
					else:
						self.functionCall += '1){\n'
					self.functionCall += 'char outPutStr[' + str(len(cmdString)+30) + '];\n' + \
																'snprintf(outPutStr,' + str(len(cmdString)+30) + ',"export HRP_DB=%f;' + cmdString + '",(float)block' + self.blockNumber + '_double_i1);' + \
																'system(outPutStr);}\n' + \
                               'block' + self.blockNumber + '_double_o1 = block' + self.blockNumber + '_double_i1;\n'
					self.dealloc = '//nothing to deallocate\n'
#############################################################################
        elif self.blockType == '602': #Analyses images for presence of circles..
					for propIter in self.properties:
						if propIter[0] == 'dpSel':
							dpSel = propIter[1]
						elif propIter[0] == 'distSel':
							distSel = propIter[1]
						elif propIter[0] == 'threshSel':
							threshSel = propIter[1]
						elif propIter[0] == 'qualySel':
							qualySel = propIter[1]
						elif propIter[0] == 'minX':
							minX = propIter[1]
						elif propIter[0] == 'maxX':
							maxX = propIter[1]
						elif propIter[0] == 'minY':
							minY = propIter[1]
						elif propIter[0] == 'maxY':
							maxY = propIter[1]
						elif propIter[0] == 'minRad':
							minRad = propIter[1]
						elif propIter[0] == 'maxRad':
							maxRad = propIter[1]
						elif propIter[0] == 'numOfCircs':
							numOfCircs = propIter[1]
						elif propIter[0] == 'criteria':
							checkCrit = propIter[1]

					if checkCrit == 'pos':
						circType = 0
					elif checkCrit == 'num':
						circType = 1

					self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
													'IplImage * block' + self.blockNumber + '_img_t1 = NULL;\n' + \
													'CvSeq * block' + self.blockNumber + '_circs = NULL;\n' + \
													'float * PCircs' + self.blockNumber + ' = NULL;\n' + \
													'CvMemStorage * block' + self.blockNumber + '_storage = NULL;\n' + \
													'int block' + self.blockNumber + '_it;\n' + \
													'IplImage * block' + self.blockNumber + '_img_o2 = NULL;\n' + \
                          'double block' + self.blockNumber + '_double_o1;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
															'	block' + self.blockNumber + '_storage = cvCreateMemStorage(0);\n' + \
															'	block' + self.blockNumber + '_img_t1 = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1),8,1);\n' + \
															'	if(block' + self.blockNumber + '_img_i1->nChannels != 1)\n' + \
															'		cvCvtColor(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_t1, CV_BGR2GRAY);\n' + \
															'	else\n' + \
															'		cvCopyImage(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_t1);\n' + \
															'	cvSmooth(block' + self.blockNumber + '_img_t1, block' + self.blockNumber + '_img_t1, CV_GAUSSIAN, 9, 9, 0,0 );\n' + \
															'	block' + self.blockNumber + '_circs = cvHoughCircles( block' + self.blockNumber + '_img_t1, block' + self.blockNumber + '_storage, CV_HOUGH_GRADIENT, ' + dpSel + ', ' + distSel + ', ' + threshSel + ', ' + qualySel + ',0,1000);\n' + \
															'	block' + self.blockNumber + '_double_o1 = 0;\n'
					if circType == 0 :
						self.functionCall += '	for(block' + self.blockNumber + '_it = 0; block' + self.blockNumber + '_it < block' + self.blockNumber + '_circs->total;block' + self.blockNumber + '_it++){\n' + \
																'		PCircs' + self.blockNumber + ' = (float*)cvGetSeqElem( block' + self.blockNumber + '_circs, block' + self.blockNumber + '_it );\n' + \
																'		if(cvRound(PCircs' + self.blockNumber + '[2]) > ' + minRad + ' && cvRound(PCircs' + self.blockNumber + '[2]) < ' + maxRad + ')\n' + \
																'			if( cvRound(PCircs' + self.blockNumber + '[0]) > ' + minX + ' && cvRound(PCircs' + self.blockNumber + '[0]) < ' + maxX + ')\n'+ \
																'				if(cvRound(PCircs' + self.blockNumber + '[1]) > ' + minY + ' && cvRound(PCircs' + self.blockNumber + '[1]) < ' + maxY + ')\n' + \
																'					block' + self.blockNumber + '_double_o1 = 1.0;\n' + \
																'	}\n'
					else :
						self.functionCall += '	if(block' + self.blockNumber + '_circs->total >= ' + str(int(float(numOfCircs))) + ')\n' + \
																'		block' + self.blockNumber + '_double_o1 = 1.0;\n'

					self.functionCall += '	block' + self.blockNumber + '_img_o2 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
																'	for(block' + self.blockNumber + '_it = 0; block' + self.blockNumber + '_it < block' + self.blockNumber + '_circs->total;block' + self.blockNumber + '_it++){\n' + \
															 '		PCircs' + self.blockNumber + ' = (float*)cvGetSeqElem( block' + self.blockNumber + '_circs, block' + self.blockNumber + '_it );\n' + \
															 '		cvCircle( block' + self.blockNumber + '_img_o2, cvPoint(cvRound(PCircs' + self.blockNumber + '[0]),cvRound(PCircs' + self.blockNumber + '[1])), cvRound(PCircs' + self.blockNumber + '[2]), CV_RGB(255,0,0), 3, 8, 0 );\n' + \
															'	}\n'

					self.functionCall +='}\n'
					
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o2);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_t1);\n' + \
													'cvReleaseMemStorage(&block' + self.blockNumber + '_storage);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
#############################################################################
        elif self.blockType == '603': #Analyses images for presence of lines..
					for propIter in self.properties:
						if propIter[0] == 'qThresh':
							qThresh = propIter[1]
						elif propIter[0] == 'minC':
							minC = propIter[1]
						elif propIter[0] == 'maxG':
							maxG = propIter[1]
						elif propIter[0] == 'aX':
							aX = propIter[1]
						elif propIter[0] == 'aY':
							aY = propIter[1]
						elif propIter[0] == 'aR':
							aR = propIter[1]
						elif propIter[0] == 'bX':
							bX = propIter[1]
						elif propIter[0] == 'bY':
							bY = propIter[1]
						elif propIter[0] == 'bR':
							bR = propIter[1]
						elif propIter[0] == 'disDraw':
							disDraw = propIter[1]

					self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
													'IplImage * block' + self.blockNumber + '_img_t1 = NULL;\n' + \
													'CvSeq * block' + self.blockNumber + '_lines = NULL;\n' + \
													'CvMemStorage * block' + self.blockNumber + '_storage = NULL;\n' + \
													'int block' + self.blockNumber + '_it;\n' + \
													'IplImage * block' + self.blockNumber + '_img_o2 = NULL;\n' + \
                          'double block' + self.blockNumber + '_double_o1;\n' + \
													'int b' + self.blockNumber + 'dX,b' + self.blockNumber + 'dY;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
															'	block' + self.blockNumber + '_storage = cvCreateMemStorage(0);\n' + \
															'	block' + self.blockNumber + '_img_t1 = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1),8,1);\n' + \
															'	if(block' + self.blockNumber + '_img_i1->nChannels != 1)\n' + \
															'		cvCvtColor(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_t1, CV_BGR2GRAY);\n' + \
															'	else\n' + \
															'		cvCopyImage(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_t1);\n' + \
															'	cvCanny(block' + self.blockNumber + '_img_t1, block' + self.blockNumber + '_img_t1, 50, 200, 3);\n' + \
															'	block' + self.blockNumber + '_lines = cvHoughLines2( block' + self.blockNumber + '_img_t1, block' + self.blockNumber + '_storage, CV_HOUGH_PROBABILISTIC, 1, CV_PI/180, '+ qThresh + ', ' + minC + ', ' + maxG + ' );\n' + \
															'	block' + self.blockNumber + '_double_o1 = 0;\n' + \
															'	for(block' + self.blockNumber + '_it = 0; block' + self.blockNumber + '_it < block' + self.blockNumber + '_lines->total;block' + self.blockNumber + '_it++)\n' + \
															'	{\n' + \
															'		CvPoint* line = (CvPoint*)cvGetSeqElem( block' + self.blockNumber + '_lines, block' + self.blockNumber + '_it );\n' + \
															'		b' + self.blockNumber + 'dX = line[0].x - ' + aX + ';\n' + \
															'		b' + self.blockNumber + 'dY = line[0].y - ' + aY + ';\n' + \
															'		if((int)cvSqrt((float)(b' + self.blockNumber + 'dX*b' + self.blockNumber + 'dX + b' + self.blockNumber + 'dY*b' + self.blockNumber + 'dY)) <= ' + aR + ')\n' + \
															'		{\n' + \
															'			b' + self.blockNumber + 'dX = line[1].x - ' + bX + ';\n' + \
															'			b' + self.blockNumber + 'dY = line[1].y - ' + bY + ';\n' + \
															'			if((int)cvSqrt((float)(b' + self.blockNumber + 'dX*b' + self.blockNumber + 'dX + b' + self.blockNumber + 'dY*b' + self.blockNumber + 'dY)) <= ' + bR + ')\n' + \
															'				block' + self.blockNumber + '_double_o1 = 1.0;\n' + \
															'		}\n' + \
															'	}\n'
					if disDraw == "no":
						self.functionCall += '	block' + self.blockNumber + '_img_o2 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
																	'	for(block' + self.blockNumber + '_it = 0; block' + self.blockNumber + '_it < block' + self.blockNumber + '_lines->total;block' + self.blockNumber + '_it++)\n	{\n' + \
															    '		CvPoint* line = (CvPoint*)cvGetSeqElem( block' + self.blockNumber + '_lines, block' + self.blockNumber + '_it );\n' + \
															   	'		cvLine( block' + self.blockNumber + '_img_o2, line[0], line[1], CV_RGB(255,0,0), 2, 8, 0);\n' + \
															'	}\n'
															
					self.functionCall += '}\n'
					
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o2);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_t1);\n' + \
													'cvReleaseMemStorage(&block' + self.blockNumber + '_storage);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'

#############################################################################
        elif self.blockType == '604': #Resizes input image using "method" to desired dim..
					for propIter in self.properties:
						if propIter[0] == 'method':
							interMethod = propIter[1]

					self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
													'CvRect block' + self.blockNumber + '_rect_i2;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
															'	block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + '_rect_i2.width,block' + self.blockNumber + '_rect_i2.height),block' + self.blockNumber + '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															'	cvResize(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_o1, ' + interMethod + ');\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'

#############################################################################
        elif self.blockType == '605': #Finds the best matchings between image (in1) and template (in2)
					for propIter in self.properties:
						if propIter[0] == 'method':
							interMethod = propIter[1]
						if propIter[0] == "scaleFactor":
							scaleFactor = propIter[1]

					self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
													'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' + \
													'IplImage * block' + self.blockNumber + '_img_t1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1 && block' + self.blockNumber + '_img_i2)\n' + \
															'{\n' + \
															'	block' + self.blockNumber + '_img_t1 = cvCreateImage(cvSize(block' + self.blockNumber + '_img_i1->width - block' + self.blockNumber + '_img_i2->width +1,block' + self.blockNumber + '_img_i1->height - block' + self.blockNumber + '_img_i2->height +1),32,1);\n' + \
															'	block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + '_img_i1->width - block' + self.blockNumber + '_img_i2->width +1,block' + self.blockNumber + '_img_i1->height - block' + self.blockNumber + '_img_i2->height +1),8,1);\n' + \
															'	cvMatchTemplate(block' + self.blockNumber + '_img_i1 , block' + self.blockNumber + '_img_i2, block' + self.blockNumber + '_img_t1, ' + interMethod + ');\n' + \
															'	cvConvertScale(block' + self.blockNumber + '_img_t1,block' + self.blockNumber + '_img_o1, ' + str(10**-(int(float(scaleFactor)))) + ',0);\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_t1);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'

#############################################################################
        elif self.blockType == '606': #Finds min or max of the Image
					for propIter in self.properties:
						if propIter[0] == 'minX':
							minX = propIter[1]
						elif propIter[0] == 'maxX':
							maxX = propIter[1]
						elif propIter[0] == 'minY':
							minY = propIter[1]
						elif propIter[0] == 'maxY':
							maxY = propIter[1]
						elif propIter[0] == 'minVal':
							minVal = propIter[1]
						elif propIter[0] == 'maxVal':
							maxVal = propIter[1]
						elif propIter[0] == 'minORmax':
							minORmax = propIter[1]
						elif propIter[0] == 'criteria':
							checkCrit = propIter[1]
					self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'double block' + self.blockNumber + '_double_o1;\n' + \
                          'CvPoint block' + self.blockNumber + '_point_o2 = cvPoint(0,0);\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1)\n{\n' + \
															'	double minVal,maxVal;\n' + \
															'	CvPoint minP,maxP;\n' + \
															'	block' + self.blockNumber + '_double_o1 = 0;\n' + \
															'	cvMinMaxLoc(block' + self.blockNumber + '_img_i1, &minVal, &maxVal, &minP, &maxP, NULL);\n'
					if minORmax == 'max':
						self.functionCall += '	minP = maxP;\n	minVal = maxVal;\n'
					
					self.functionCall += '	block' + self.blockNumber + '_point_o2 = minP;\n'
					
					if checkCrit == "pos":
						self.functionCall += '	if(minP.x >= ' + minX + ' && minP.x <= ' + maxX + ')\n' + \
																	'		if(minP.y >= ' + minY + ' && minP.y <= ' + maxY + ')\n' + \
																	'			block' + self.blockNumber + '_double_o1 = 1.0;\n'
					elif checkCrit == "val":
						self.functionCall += '	if(minVal >= ' + minVal + ' && minVal <= ' + maxVal + ')\n' + \
																	'		block' + self.blockNumber + '_double_o1 = 1.0;\n'
					self.functionCall += '}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'

#############################################################################
        elif self.blockType == '607': #Rotates input image
					for propIter in self.properties:
						if propIter[0] == 'xC':
							xC = propIter[1]
						elif propIter[0] == 'yC':
							yC = propIter[1]
						elif propIter[0] == 'isFilling':
							isFilling = propIter[1]
						elif propIter[0] == 'isCenter':
							isCenter = propIter[1]
						elif propIter[0] == 'isScalling':
							isScalling = propIter[1]
					
					self.imagesIO = '\nIplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'double block' + self.blockNumber + '_double_i2;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n'
					self.functionCall = '\n	if(block' + self.blockNumber + '_img_i1)\n	{\n' + \
															'		double scale;\n	int H;\n	int W;\n' + \
															'		W = block' + self.blockNumber + '_img_i1->width;\n' + \
															'		H = block' + self.blockNumber + '_img_i1->height;\n' + \
															'		block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(W,H),block' + self.blockNumber + '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' + \
															'		CvMat* mat = cvCreateMat(2,3,CV_32FC1);\n'
					if isCenter == "true":
						self.functionCall += '		CvPoint2D32f center = cvPoint2D32f(W/2, H/2);\n'
					else:
						self.functionCall += '		CvPoint2D32f center = cvPoint2D32f(' + str(int(float(xC))) + ',' + str(int(float(yC))) + ');\n'

					if isScalling == "true":
						self.functionCall += '		scale = H/(fabs(H*sin(rads(90-abs(block' + self.blockNumber + '_double_i2)))) + fabs(W*sin(rads(abs(block' + self.blockNumber + '_double_i2)))));\n' + \
															'		cv2DRotationMatrix(center,block' + self.blockNumber + '_double_i2,scale,mat);\n'
					else:
						self.functionCall += '		cv2DRotationMatrix(center,block' + self.blockNumber + '_double_i2,1.0,mat);\n'
															
					if isFilling == "true":
						self.functionCall += '		cvWarpAffine(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o1,mat,CV_WARP_FILL_OUTLIERS,cvScalarAll(0));\n'
					else:
						self.functionCall += '		cvWarpAffine(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o1,mat,0,cvScalarAll(0));\n'
						
					self.functionCall += '	}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'

#############################################################################
        elif self.blockType == '04': #EQUALIZE HIST
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_SourceCx[3];\n' + \
                          'IplImage * block' + self.blockNumber + '_EqCx[3];\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' + \
                              'block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 3);\n' + \
                              'block' + self.blockNumber + '_SourceCx[0] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              'block' + self.blockNumber + '_SourceCx[1] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              'block' + self.blockNumber + '_SourceCx[2] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              'block' + self.blockNumber + '_EqCx[0] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              'block' + self.blockNumber + '_EqCx[1] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              'block' + self.blockNumber + '_EqCx[2] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              'cvSplit(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_SourceCx[0],' + \
                              'block' + self.blockNumber + '_SourceCx[1],block' + self.blockNumber + '_SourceCx[2], NULL);\n' + \
                              'cvEqualizeHist(block' + self.blockNumber + '_SourceCx[0], block' + self.blockNumber + '_EqCx[0]);\n' + \
                              'cvEqualizeHist(block' + self.blockNumber + '_SourceCx[1], block' + self.blockNumber + '_EqCx[1]);\n' + \
                              'cvEqualizeHist(block' + self.blockNumber + '_SourceCx[2], block' + self.blockNumber + '_EqCx[2]);\n' + \
                              'cvMerge( block' + self.blockNumber + '_EqCx[0],block' + self.blockNumber + '_EqCx[1],' + \
                              'block' + self.blockNumber + '_EqCx[2], NULL,block' + self.blockNumber + '_img_o1);\n' + \
                              'cvReleaseImage(&block' + self.blockNumber + '_SourceCx[0]);\n' + \
                              'cvReleaseImage(&block' + self.blockNumber + '_SourceCx[1]);\n' + \
                              'cvReleaseImage(&block' + self.blockNumber + '_SourceCx[2]);\n' + \
                              'cvReleaseImage(&block' + self.blockNumber + '_EqCx[0]);\n' + \
                              'cvReleaseImage(&block' + self.blockNumber + '_EqCx[1]);\n' + \
                              'cvReleaseImage(&block' + self.blockNumber + '_EqCx[2]);\n' + \
                              '}\n'
            self.dealloc = 	'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
															'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'

##################################################################
################## Do not add nor remove any lines before this..  doing patches on line 1066





































########## liveDelay #######################
        elif self.blockType == '12': # Live Delay brief description
					for propIter in self.properties:
						if propIter[0] == 'type':
							delayType = propIter[1]
						elif propIter[0] == 'frameNumber':
							frameNumber = int(float(propIter[1]))
							frameNumber = max(frameNumber,1)
					self.imagesIO = 'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'int block' + self.blockNumber + '_t_idx = 0;\n' + \
                          'IplImage * block' + self.blockNumber + '_buffer[' + str(frameNumber) + '] = {'
					for idx in range(frameNumber):
						self.imagesIO += 'NULL'
						if idx <> frameNumber-1:
							self.imagesIO += ','
					self.imagesIO += '};\n'
					
					for idx in range(frameNumber):
						self.imagesIO += 'block' + self.blockNumber + '_buffer[' + str(idx) + '] = cvCreateImage( cvSize(640,480), 8, 3);\n'
						self.imagesIO += 'cvSetZero(block' + self.blockNumber + '_buffer[' + str(idx) + ']);\n'
					self.imagesIO += 'block' + self.blockNumber + '_img_o1 = block' + self.blockNumber + '_buffer[' + str(frameNumber-1) + '];\n'
					
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1)\n{\n' +  \
															'	cvReleaseImage(&(block' + self.blockNumber + '_buffer[block' + self.blockNumber + '_t_idx]));\n' + \
															'	block' + self.blockNumber + '_buffer[block' + self.blockNumber + '_t_idx] = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
															'	block' + self.blockNumber + '_t_idx++;\n' + \
															'	block' + self.blockNumber + '_t_idx %= ' + str(frameNumber) + ';\n' + \
															'	block' + self.blockNumber + '_img_o1 = block' + self.blockNumber + '_buffer[block' + self.blockNumber + '_t_idx];\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'
					self.outDealloc = 'for(block' + self.blockNumber + '_t_idx=0;block' + self.blockNumber + '_t_idx<' + str(frameNumber) + ';block' + self.blockNumber + '_t_idx++)\n' + \
														'	if(block' + self.blockNumber + '_buffer[block' + self.blockNumber + '_t_idx] != NULL)\n' + \
														'		cvReleaseImage(&(block' + self.blockNumber + '_buffer[block' + self.blockNumber + '_t_idx]));\n'

########## GetSize #######################
        elif self.blockType == '13': # Get Size
					#for propIter in self.properties:
						#if propIter[0] == 'type':
							#delayType = propIter[1]
						#elif propIter[0] == 'frameNumber':
							#frameNumber = int(float(propIter[1]))
							#frameNumber = max(frameNumber,1)
					self.imagesIO = 'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'CvRect block' + self.blockNumber + '_rect_o1 = cvRect( 0, 0, 1, 1);\n'

					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1)\n{\n' +  \
															'	block' + self.blockNumber + '_rect_o1 = cvRect( 0, 0, block' + self.blockNumber + '_img_i1->width, block' + self.blockNumber + '_img_i1->height);\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'


########## stereoCorr #######################
        elif self.blockType == '611': # Stereo Correspondence brief description 
					for propIter in self.properties:
						if propIter[0] == 'maxDist':
							maxDist = propIter[1]
					self.imagesIO =  \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' +  \
                          'IplImage * block' + self.blockNumber + '_img_i2 = NULL;\n' +  \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_ts1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_ts2 = NULL;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1 && block' + self.blockNumber + '_img_i2)\n{\n' +  \
															'	if(!block' + self.blockNumber + '_img_o1)\n' + \
															'		block' + self.blockNumber + '_img_o1 = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1), IPL_DEPTH_8U, 1);\n' +  \
															'	if(!block' + self.blockNumber + '_img_ts1)\n' + \
															'		block' + self.blockNumber + '_img_ts1 = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1), IPL_DEPTH_8U, 1);\n' + \
															'	if(!block' + self.blockNumber + '_img_ts2)\n' + \
															'		block' + self.blockNumber + '_img_ts2 = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1), IPL_DEPTH_8U, 1);\n' + \
															'	cvCvtColor(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_ts1, CV_BGR2GRAY);\n' + \
															'	cvCvtColor(block' + self.blockNumber + '_img_i2, block' + self.blockNumber + '_img_ts2, CV_BGR2GRAY);\n' + \
															'	cvFindStereoCorrespondence( block' + self.blockNumber + '_img_ts1, block' + self.blockNumber + '_img_ts2, CV_DISPARITY_BIRCHFIELD, block' + self.blockNumber + '_img_o1, ' + maxDist + ', 15, 3, 6, 8, 15 );\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' +  \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i2);\n' + \
													'if(block' + self.blockNumber + '_img_ts1)\n\tcvReleaseImage(&block' + self.blockNumber + '_img_ts1);\n' + \
													'if(block' + self.blockNumber + '_img_ts2)\n\tcvReleaseImage(&block' + self.blockNumber + '_img_ts2);\n'

########## saveVideo #######################
        elif self.blockType == '11': # Save Video brief description 
					global g_bSaveVideo
					g_bSaveVideo.append(self.blockNumber)
					for propIter in self.properties:
						if propIter[0] == 'filename':
							videoFilename = os.path.expanduser(propIter[1])
						if propIter[0] == 'framerate':
							frameRate = propIter[1]
						if propIter[0] == 'codecSelection':
							codecMacro = 'CV_FOURCC(\'P\',\'I\',\'M\',\'2\')'
							if propIter[1] == "MPEG1":
								codecMacro = 'CV_FOURCC(\'P\',\'I\',\'M\',\'2\')'
							if propIter[1] == "mjpeg":
								codecMacro = 'CV_FOURCC(\'M\',\'J\',\'P\',\'G\')'
							if propIter[1] == "MPEG4.2":
								codecMacro = 'CV_FOURCC(\'M\',\'P\',\'4\',\'2\')'
							if propIter[1] == "MPEG4.3":
								codecMacro = 'CV_FOURCC(\'D\',\'I\',\'V\',\'3\')'
							if propIter[1] == "MPEG4":
								codecMacro = 'CV_FOURCC(\'D\',\'I\',\'V\',\'X\')'
							if propIter[1] == "H263":
								codecMacro = 'CV_FOURCC(\'U\',\'2\',\'6\',\'3\')'
							if propIter[1] == "H263I":
								codecMacro = 'CV_FOURCC(\'I\',\'2\',\'6\',\'3\')'
							if propIter[1] == "FLV1":
								codecMacro = 'CV_FOURCC(\'F\',\'L\',\'V\',\'1\')'
					self.imagesIO =  'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
													 'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
													 'CvVideoWriter* block' + self.blockNumber + '_vidWriter = NULL;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' +  \
															'	if(block' + self.blockNumber + '_vidWriter == NULL)//video writer not started up yet!\n' + \
															'		block' + self.blockNumber + '_vidWriter = cvCreateVideoWriter( "' + videoFilename + '", ' + codecMacro + ',' + frameRate + ', cvGetSize(block' + self.blockNumber + '_img_i1), 1 );\n' + \
															'	cvWriteFrame( block' + self.blockNumber + '_vidWriter, block' + self.blockNumber + '_img_i1);\n' + \
															'	block' + self.blockNumber + '_img_o1 = block' + self.blockNumber + '_img_i1;\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'





########## haarDetect #######################
        elif self.blockType == '610': # Haar (face) Detector brief description 
					for propIter in self.properties:
						if propIter[0] == 'cascade_name':
							cascade_name = os.path.expanduser(propIter[1])
						elif propIter[0] == 'min_neighbors':
							t_sMinNeighbors = propIter[1]
					self.imagesIO =  \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' +  \
                          'CvPoint block' + self.blockNumber + '_point_o1 = cvPoint(0,0);\n' +  \
													'CvRect block' + self.blockNumber + '_rect_o2 = cvRect( 0, 0, 1, 1);\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o3 = NULL;\n' + \
													'double block' + self.blockNumber + '_double_o4 = 0.0;\n' + \
                          'static CvMemStorage* block' + self.blockNumber + '_storage = 0;\n' + \
                          'static CvHaarClassifierCascade* block' + self.blockNumber + '_cascade = 0;\n' + \
                          'const char* block' + self.blockNumber + '_cascade_name = "' + cascade_name + '";\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' +  \
															'	double scale = 1.3;\n' + \
															'	block' + self.blockNumber + '_cascade = (CvHaarClassifierCascade*)cvLoad( block' + self.blockNumber + '_cascade_name, 0, 0, 0 );\n' + \
															'	IplImage* gray = cvCreateImage( cvSize(block' + self.blockNumber + '_img_i1->width,block' + self.blockNumber + '_img_i1->height), 8, 1 );\n' + \
															'	IplImage* small_img = cvCreateImage( cvSize( cvRound (block' + self.blockNumber + '_img_i1->width/scale), cvRound (block' + self.blockNumber + '_img_i1->height/scale)),8, 1 );\n' + \
															'	cvCvtColor( block' + self.blockNumber + '_img_i1, gray, CV_BGR2GRAY );\n' + \
															'	cvResize( gray, small_img, CV_INTER_LINEAR );\n' + \
															'	cvEqualizeHist( small_img, small_img );\n' + \
															'	if(!block' + self.blockNumber +'_img_o3)\n' + \
															'	block' + self.blockNumber + '_img_o3 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
															'	cvCopy(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o3,0);\n' + \
															'	block' + self.blockNumber + '_storage = cvCreateMemStorage(0);\n' + \
															'	cvClearMemStorage( block' + self.blockNumber + '_storage );\n' + \
															'	block' + self.blockNumber + '_rect_o2 = cvRect( 0, 0, 1, 1);\n' + \
															'	CvSeq* faces = cvHaarDetectObjects( small_img, block' + self.blockNumber + '_cascade, block' + self.blockNumber + '_storage,1.1, ' + t_sMinNeighbors + ', 0/*CV_HAAR_DO_CANNY_PRUNING*/,cvSize(30, 30) );\n' + \
															'	block' + self.blockNumber + '_double_o4 = faces->total;\n' + \
															'	if(faces)\n' + \
															'	{\n' + \
															'		int i;\n' + \
															'		for( i = 0; i < (faces ? faces->total : 0); i++ )\n' + \
															'		{\n' + \
															'		CvRect* r = (CvRect*)cvGetSeqElem( faces, i );\n' + \
															'			if(r)\n' + \
															'			{\n' + \
															'				CvPoint center;\n' + \
															'				int radius;\n' + \
															'				center.x = cvRound((r->x + r->width*0.5)*scale);\n' + \
															'				center.y = cvRound((r->y + r->height*0.5)*scale);\n' + \
															'				radius = cvRound((r->width + r->height)*0.25*scale);\n' + \
															'				cvCircle( block' + self.blockNumber + '_img_o3, center, radius, cvScalarAll(0), 3, 8, 0 );\n' + \
															'				if(i == 0)\n' + \
															'				{\n' + \
															'					block' + self.blockNumber + '_point_o1 = center;\n' + \
															'					block' + self.blockNumber + '_rect_o2.x = (r->x)*scale;\n' + \
															'					block' + self.blockNumber + '_rect_o2.y = (r->y)*scale;\n' + \
															'					block' + self.blockNumber + '_rect_o2.width = (r->width)*scale;\n' + \
															'					block' + self.blockNumber + '_rect_o2.height = (r->height)*scale;\n' + \
															'				}\n' + \
															'			}\n' + \
															'		}\n' + \
															'	}\n' + \
															'	cvReleaseImage( &gray );\n' + \
															'	cvReleaseImage( &small_img );\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o3);\n' +  \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
													'cvReleaseMemStorage(&block' + self.blockNumber + '_storage);\n'



########## findColor #######################
        elif self.blockType == '609': # Find object of a given color brief description 
					for propIter in self.properties:
						if propIter[0] == '_B':
							c_B = propIter[1]
						elif propIter[0] == '_B_T':
							c_B_T = propIter[1]
						elif propIter[0] == '_G':
							c_G = propIter[1]
						elif propIter[0] == '_G_T':
							c_G_T = propIter[1]
						elif propIter[0] == '_R':
							c_R = propIter[1]
						elif propIter[0] == '_R_T':
							c_R_T = propIter[1]

					global usesFindColor
					usesFindColor = 1
					#o1 - pto
					#o2 - numOfPoints
					#o3 - variance
					#o4 - img
					self.imagesIO =  \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o4 = NULL;\n' + \
													'CvPoint block' + self.blockNumber + '_point_o1;\n' + \
													'uchar block' + self.blockNumber + 'c_value[3] = {' + c_B + ',' + c_G + ',' + c_R + '};\n' + \
													'uchar block' + self.blockNumber + 'tolerance[3] = {' + c_B_T + ',' + c_G_T + ',' + c_R_T + '};\n' + \
													'double block' + self.blockNumber + '_double_o2;\n' + \
													'double block' + self.blockNumber + '_double_o3;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' +  \
															'	IplImage * block' + self.blockNumber + '_img_t1 = cvCreateImage(cvGetSize(block' + self.blockNumber + '_img_i1),IPL_DEPTH_8U, 1);\n' + \
															'	if(!block' + self.blockNumber + '_img_o4)\n' + \
															'		block' + self.blockNumber + '_img_o4 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' + \
															'	else\n' + \
															' 	cvCopy(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o4,0);\n' + \
															'	block' + self.blockNumber + '_double_o2 = CheckForColor(block' + self.blockNumber + '_img_i1, block' + self.blockNumber + '_img_t1, block' + self.blockNumber + 'c_value, block' + self.blockNumber + 'tolerance, &block' + self.blockNumber + '_point_o1, &block' + self.blockNumber + '_double_o3);\n' + \
															'	cvCircle(block' + self.blockNumber + '_img_o4,block' + self.blockNumber + '_point_o1,8,cvScalarAll(255),4,8,0);\n' + \
															'	cvReleaseImage(&block' + self.blockNumber + '_img_t1);\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o4);\n' +  \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'






########## findSquares #######################
        elif self.blockType == '608': # Find Squares brief description 
					global usesFindSquares
					usesFindSquares = 1
					for propIter in self.properties:
						if propIter[0] == 'enMin':
							enMin = (propIter[1] == "True")
						if propIter[0] == 'enMax':
							enMax = (propIter[1] == "True")
						if propIter[0] == 'minVal':
							minVal = propIter[1]
						if propIter[0] == 'maxVal':
							maxVal = propIter[1]
					if not enMin:
						minVal = -1
					if not enMax:
						maxVal = -1
					self.imagesIO =  \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' +  \
                          'IplImage * block' + self.blockNumber + '_img_o2 = NULL;\n' + \
													'double block' + self.blockNumber + '_double_o1;\n' + \
													'CvMemStorage * block' + self.blockNumber + '_storage = NULL;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' +  \
															'	block' + self.blockNumber + '_img_o2 = cvCloneImage(block' + self.blockNumber + '_img_i1);\n' +  \
															'	block' + self.blockNumber + '_storage = cvCreateMemStorage(0);\n' +  \
															'	block' + self.blockNumber + '_double_o1 = (double)drawSquares( block' + self.blockNumber + '_img_o2, findSquares4( block' + self.blockNumber + '_img_o2, block' + self.blockNumber + '_storage , ' + str(minVal) + ', ' + str(maxVal) + ') );\n' +  \
															'	cvClearMemStorage( block' + self.blockNumber + '_storage );\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o2);\n' +  \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
													'cvReleaseMemStorage(&block' + self.blockNumber + '_storage );\n'






########## moveRct #######################
        elif self.blockType == '803': # Move Rectangle brief description
					for propIter in self.properties:
						if propIter[0] == 'offset_x':
							offset_x = propIter[1]
						if propIter[0] == 'offset_y':
							offset_y = propIter[1]
					self.imagesIO =  'CvRect block' + self.blockNumber + '_rect_i1;\n' +  \
                          'CvPoint block' + self.blockNumber + '_point_i2;\n' + \
                          'CvRect block' + self.blockNumber + '_rect_o1;\n'
					self.functionCall = 'block' + self.blockNumber + '_rect_o1 = block' + self.blockNumber + '_rect_i1;\n' +  \
															'block' + self.blockNumber + '_rect_o1.x = block' + self.blockNumber + '_point_i2.x + ' + offset_x + ';\n' + \
															'block' + self.blockNumber + '_rect_o1.y = block' + self.blockNumber + '_point_i2.y + ' + offset_y + ';\n'
					self.dealloc = ''


########## isOnRect #######################
        elif self.blockType == '902': # Check Point brief description 
					#for propIter in self.properties:
						#if propIter[0] == 'method':
							#interMethod = propIter[1]

					self.imagesIO = 'CvRect block' + self.blockNumber + '_rect_i2;\n' +  \
                          'CvPoint block' + self.blockNumber + '_point_i1;\n' + \
													'double block' + self.blockNumber + '_double_o1;\n'
					self.functionCall = '\n block' + self.blockNumber + '_double_o1 = 0.0;\n' + \
															'if(block' + self.blockNumber + '_point_i1.x >= block' + self.blockNumber + '_rect_i2.x)\n' +  \
															'	if(block' + self.blockNumber + '_point_i1.y >= block' + self.blockNumber + '_rect_i2.y)\n' +  \
															'		if(block' + self.blockNumber + '_point_i1.x < block' + self.blockNumber + '_rect_i2.x + block' + self.blockNumber + '_rect_i2.width)\n' +  \
															'			if(block' + self.blockNumber + '_point_i1.y < block' + self.blockNumber + '_rect_i2.y + block' + self.blockNumber + '_rect_i2.height)\n' +  \
															'				block' + self.blockNumber + '_double_o1 = 1.0;\n'
					self.dealloc = ''


########## newPoint #######################
        elif self.blockType == '901': # New Point brief description 
					for propIter in self.properties:
						if propIter[0] == 'x0':
							x0 = propIter[1]
						elif propIter[0] == 'y0':
							y0 = propIter[1]
					self.imagesIO = 'CvPoint block' + self.blockNumber + '_point_o1;\n'
					self.functionCall = 'block' + self.blockNumber + '_point_o1 = cvPoint(' + str(int(float(x0))) + ',' + str(int(float(y0))) + ');\n'
					self.dealloc = ''




########## cropImage #######################
        elif self.blockType == '802': # Crop Image brief description 
					#for propIter in self.properties:
						#if propIter[0] == 'offset_x':
							#offset_x = propIter[1]
						#if propIter[0] == 'offset_y':
							#offset_y = propIter[1]

					self.imagesIO =  \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' +  \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
													'CvRect  block' + self.blockNumber + '_rect_i2;\n'
					self.functionCall = '\nif(block' + self.blockNumber + '_img_i1){\n' +  \
															'	block' + self.blockNumber + '_rect_i2.x = MAX(0,block' + self.blockNumber + '_rect_i2.x);//Check whether point is negative\n' + \
															'	block' + self.blockNumber + '_rect_i2.y = MAX(0,block' + self.blockNumber + '_rect_i2.y);\n' + \
															'	block' + self.blockNumber + '_rect_i2.x = MIN(block' +self.blockNumber + '_img_i1->width-1,block' + self.blockNumber + '_rect_i2.x);//Check whether point is out of the image\n' + \
															'	block' + self.blockNumber + '_rect_i2.y = MIN(block' +self.blockNumber + '_img_i1->height-1,block' + self.blockNumber + '_rect_i2.y);\n' + \
															'	block' + self.blockNumber + '_rect_i2.width = MIN(block' +self.blockNumber + '_img_i1->width-block' + self.blockNumber + '_rect_i2.x,block' + self.blockNumber + '_rect_i2.width);//Check whether rect reaches out of the image\n' + \
															'	block' + self.blockNumber + '_rect_i2.height = MIN(block' +self.blockNumber + '_img_i1->height-block' + self.blockNumber + '_rect_i2.y,block' + self.blockNumber + '_rect_i2.height);\n' + \
															'	block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + self.blockNumber + '_rect_i2.width,block' + self.blockNumber + '_rect_i2.height),' + \
															' block' + self.blockNumber + '_img_i1->depth,block' + self.blockNumber + '_img_i1->nChannels);\n' +  \
															'	cvSetImageROI(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_rect_i2);\n' + \
															'	cvCopyImage(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_img_o1);\n' + \
															'}\n'
					self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' +  \
													'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'



########## newDouble #######################
        elif self.blockType == '701': # New Double Value brief description 
					for propIter in self.properties:
						if propIter[0] == 'doubleVal':
							doubleVal = propIter[1]
					self.imagesIO =  '\ndouble  block' + self.blockNumber + '_double_o1;\n'
					self.functionCall = '	block' + self.blockNumber + '_double_o1 = ' + str(float(doubleVal)) + ';\n'
					self.dealloc = ''



########## newRect #######################
        elif self.blockType == '801': # New Rectangle brief description 
					for propIter in self.properties:
						if propIter[0] == 'x0':
							x0 = propIter[1]
						elif propIter[0] == 'y0':
							y0 = propIter[1]
						elif propIter[0] == 'width':
							rctWidth = propIter[1]
						elif propIter[0] == 'height':
							rctHeight = propIter[1]
					self.imagesIO = '\nCvRect block' + self.blockNumber + '_rect_o1;\n'
					self.functionCall = 'block' + self.blockNumber + '_rect_o1 = cvRect(' + str(int(float(x0))) + ', ' + str(int(float(y0))) + ', ' + str(int(float(rctWidth))) + ', ' + str(int(float(rctHeight))) + ');'
					self.dealloc = ''





#############################################################################
        elif self.blockType == '03': #PLOT HISTOGRAM
            flag = ''
            for propIter in self.properties:
                if propIter[0] == 'type':
                    if (propIter[1] == 'allcolors'):
                      ChannelValue = '3'
                      HistValue = '0'
                      flag = 'allColors'
                    elif (propIter[1] == 'color'):
                      flag = 'oneColor'
                if ((propIter[0] == 'channel') & (flag == 'oneColor')):
                    if (propIter[1] == 'R'):
                      ChannelValue = '3'
                      HistValue = '2'
                    if (propIter[1]== 'G'):
                      ChannelValue = '2'
                      HistValue = '1'
                    if (propIter[1] == 'B'):
                      ChannelValue = '1'
                      HistValue = '0'
            self.imagesIO = \
                          'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
                          'IplImage * block' + self.blockNumber + '_img_o1 = NULL;\n' + \
                          'CvHistogram * block' + self.blockNumber + '_histogram;\n' + \
                          'IplImage * block' + self.blockNumber + '_SourceCx[] = { NULL, NULL, NULL};\n' + \
                          'IplImage * block' + self.blockNumber + '_HistCx[] = { NULL, NULL, NULL};\n' + \
                          'int block' + self.blockNumber + '_histogram_size[] = { 255, 255, 255 };\n' + \
                          'float * block' + self.blockNumber + '_hist_ranges[] = { NULL, NULL, NULL};\n' + \
                          'float block' + self.blockNumber + '_hist_rang[2];\n' + \
                          'float block' + self.blockNumber + '_histBin;\n' + \
                          'float block' + self.blockNumber + '_histMaxVal;\n' + \
                          'int block' + self.blockNumber + '_histV;\n' + \
                          'int block' + self.blockNumber + '_plotHistChanIter;\n' + \
                          'int block' + self.blockNumber + '_plotHistArrIter;\n'
            self.functionCall = '\nif(block' + self.blockNumber + '_img_i1 && block' + self.blockNumber + '_img_i1->nChannels == 3){\n' + \
                              '	block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U,3);\n' + \
                              '	block' + self.blockNumber + '_SourceCx[0] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              '	block' + self.blockNumber + '_SourceCx[1] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              '	block' + self.blockNumber + '_SourceCx[2] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              '	block' + self.blockNumber + '_HistCx[0] = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
                              '	block' + self.blockNumber + '_HistCx[1] = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
                              '	block' + self.blockNumber + '_HistCx[2] = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
                              '	cvSplit(block' + self.blockNumber + '_img_i1,block' + self.blockNumber + '_SourceCx[0],' + \
                              '	block' + self.blockNumber + '_SourceCx[1],block' + self.blockNumber + '_SourceCx[2], NULL);\n' + \
                              '	block' + self.blockNumber + '_hist_rang[0] = 0;\n' + \
                              '	block' + self.blockNumber + '_hist_rang[1] = 255;\n' + \
                              '	block' + self.blockNumber + '_hist_ranges[0] = block' + self.blockNumber + '_hist_rang;\n' + \
                              '	block' + self.blockNumber + '_hist_ranges[1] = block' + self.blockNumber + '_hist_rang;\n' + \
                              '	block' + self.blockNumber + '_hist_ranges[2] = block' + self.blockNumber + '_hist_rang;\n' + \
                              '	block' + self.blockNumber + '_histogram = cvCreateHist( 1, block' + self.blockNumber + '_histogram_size,' + \
                              ' CV_HIST_ARRAY, block' + self.blockNumber + '_hist_ranges, 1);\n' + \
                              '	for(block' + self.blockNumber + '_plotHistChanIter =' + HistValue + ';block' + self.blockNumber + '_plotHistChanIter<' + ChannelValue + ';' \
                              'block' + self.blockNumber + '_plotHistChanIter++)\n' + \
                              '	{\n' + \
                              '		cvCalcHist( &block' + self.blockNumber + '_SourceCx[block' + self.blockNumber + '_plotHistChanIter],' + \
                              'block' + self.blockNumber + '_histogram, 0,NULL);\n' + \
                              '		cvSetZero(block' + self.blockNumber + '_HistCx[block' + self.blockNumber + '_plotHistChanIter]);\n' + \
                              '		cvGetMinMaxHistValue(block' + self.blockNumber + '_histogram,0, &block' + self.blockNumber + '_histMaxVal, NULL,NULL);\n' + \
                              '		for(block' + self.blockNumber + '_plotHistArrIter=0;block' + self.blockNumber + '_plotHistArrIter<255;' + \
                              'block' + self.blockNumber + '_plotHistArrIter++)\n' + \
                              '		{\n' + \
                              '			block' + self.blockNumber + '_histBin = cvQueryHistValue_1D(block' + self.blockNumber + '_histogram,' + \
                              'block' + self.blockNumber + '_plotHistArrIter);\n' + \
                              '			block' + self.blockNumber + '_histV=(int)((block' + self.blockNumber + '_histBin/block' + self.blockNumber + '_histMaxVal)*300);\n' + \
                              '			block' + self.blockNumber + '_histV=block' + self.blockNumber + '_HistCx[block' + self.blockNumber + '_plotHistChanIter]->height - 1 - block' + self.blockNumber + '_histV;\n' + \
                              '			cvLine(block' + self.blockNumber + '_HistCx[block' + self.blockNumber + '_plotHistChanIter], cvPoint(block' + self.blockNumber + '_plotHistArrIter' + \
                              ',block' + self.blockNumber + '_histV), cvPoint(block' + self.blockNumber + '_plotHistArrIter,block' + self.blockNumber + '_HistCx[block' + self.blockNumber + '_plotHistChanIter]->height' \
                              ' - 1),cvScalarAll(255),1, CV_AA,0 );' + \
                              '		}\n' + \
                              '	}\n' + \
                              '	cvMerge(block' + self.blockNumber + '_HistCx[0],' + \
                              'block' + self.blockNumber + '_HistCx[1],block' + self.blockNumber + '_HistCx[2],' + \
                              ' NULL,block' + self.blockNumber + '_img_o1);\n' + \
                              '}\n' + \
                              'else\n' + \
                              '{\n' + \
                              '	block' + self.blockNumber + '_img_o1 = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U,1);\n' + \
                              '	block' + self.blockNumber + '_SourceCx[0] = cvCreateImage(cvSize(block' + self.blockNumber + \
                              '_img_i1->width,block' + self.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                              '	block' + self.blockNumber + '_hist_rang[0] = 0;\n' + \
                              '	block' + self.blockNumber + '_hist_rang[1] = 255;\n' + \
                              '	block' + self.blockNumber + '_hist_ranges[0] = block' + self.blockNumber + '_hist_rang;\n' + \
                              '	block' + self.blockNumber + '_histogram = cvCreateHist( 1, block' + self.blockNumber + '_histogram_size,' + \
                              ' CV_HIST_ARRAY, block' + self.blockNumber + '_hist_ranges, 1);\n' + \
                              '	cvCalcHist( &block' + self.blockNumber + '_SourceCx[0], block' + self.blockNumber + '_histogram, 0,NULL);\n' + \
                              '	cvSetZero(block' + self.blockNumber + '_img_o1);\n' + \
                              '	cvGetMinMaxHistValue(block' + self.blockNumber + '_histogram,0, &block' + self.blockNumber + '_histMaxVal, NULL,NULL);\n' + \
                              '	for(block' + self.blockNumber + '_plotHistArrIter=0;block' + self.blockNumber + '_plotHistArrIter<255;block' + self.blockNumber + '_plotHistArrIter++)\n' + \
                              '	{\n' + \
                              '		block' + self.blockNumber + '_histBin = cvQueryHistValue_1D(block' + self.blockNumber + '_histogram, block' + self.blockNumber + '_plotHistArrIter);\n' + \
                              '		block' + self.blockNumber + '_histV=(int)((block' + self.blockNumber + '_histBin/block' + self.blockNumber + '_histMaxVal)*300);\n' + \
                              '		block' + self.blockNumber + '_histV=block' + self.blockNumber + '_img_o1->height - 1 - block' + self.blockNumber + '_histV;\n' + \
                              '		cvLine(block' + self.blockNumber + '_img_o1, cvPoint(block' + self.blockNumber + '_plotHistArrIter ,block' + self.blockNumber + '_histV), cvPoint(block' + self.blockNumber + '_plotHistArrIter,block' + self.blockNumber + '_img_o1->height' \
                              ' - 1),cvScalarAll(255),1, 0,0 );\n' + \
                              '	}\n' + \
                              '}\n'
            self.dealloc = 'if(block' + self.blockNumber + '_SourceCx[0]) cvReleaseImage(&block' + self.blockNumber + '_SourceCx[0]);\n' + \
                              'if(block' + self.blockNumber + '_SourceCx[1]) cvReleaseImage(&block' + self.blockNumber + '_SourceCx[1]);\n' + \
                              'if(block' + self.blockNumber + '_SourceCx[2]) cvReleaseImage(&block' + self.blockNumber + '_SourceCx[2]);\n' + \
                              'if(block' + self.blockNumber + '_HistCx[0]) cvReleaseImage(&block' + self.blockNumber + '_HistCx[0]);\n' + \
                              'if(block' + self.blockNumber + '_HistCx[1]) cvReleaseImage(&block' + self.blockNumber + '_HistCx[1]);\n' + \
                              'if(block' + self.blockNumber + '_HistCx[2]) cvReleaseImage(&block' + self.blockNumber + '_HistCx[2]);\n' + \
                              'if(block' + self.blockNumber + '_img_i1) cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n' + \
                              'if(block' + self.blockNumber + '_img_o1) cvReleaseImage(&block' + self.blockNumber + '_img_o1);\n' + \
                              'cvReleaseHist(&block' + self.blockNumber + '_histogram);\n'
############################ connectors ####################################
# THIS CODE IS RESPONSIBLE FOR CREATING THE ASSIGNMENTS BETWEEN THE IMAGES #
############################################################################
#It works simply by copying all the content resulting from it's processing to feed another image.
    def connectorCodeWriter(self):
        global g_bLive
        global g_flagFrame
        global g_bSaveVideo
        for x in self.myConnections:
            if x.destinationNumber <> '--':
              ##### cpscotti typed connections..
              if x.connType == "HRP_IMAGE":
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(block' + self.blockNumber + '_img_o' + x.sourceOutput + ');// IMAGE conection\n'
              elif x.connType == "HRP_INT":
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_int_i' + x.destinationInput + ' = block' + self.blockNumber + '_int_o' + x.sourceOutput + ';// INT conection\n'
              elif x.connType == "HRP_POINT":
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_point_i' + x.destinationInput + ' = block' + self.blockNumber + '_point_o' + x.sourceOutput + ';// POINT conection\n'
              elif x.connType == "HRP_RECT":
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_rect_i' + x.destinationInput + ' = block' + self.blockNumber + '_rect_o' + x.sourceOutput + ';// RECT conection\n'
              elif x.connType == "HRP_DOUBLE":
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_double_i' + x.destinationInput + ' = block' + self.blockNumber + '_double_o' + x.sourceOutput + ';// DOUBLE conection\n'
              elif x.connType == "HRP_SIZE":
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_size_i' + x.destinationInput + ' = block' + self.blockNumber + '_size_o' + x.sourceOutput + ';// SIZE conection\n'
              else:
                self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(block' + self.blockNumber + '_img_o' + x.sourceOutput + ');// IMAGE conection\n'
               # if ( (not g_bLive) or (g_flagFrame == 0) ):
                #self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(block' + self.blockNumber + '_img_o' + x.sourceOutput + ');//conection\n'
                #elif g_flagFrame:
                 #   self.functionCall = self.functionCall + 'block' + x.destinationNumber + '_img_i' + x.destinationInput + ' = cvCloneImage(frame);//conection\n'
                 #   global g_flagFrame
                 #   g_flagFrame = 0
############################################################################


#############################   savers   #######################################
# THIS CODE IS TO SAVE IMAGES THAT WILL BE RETURNED AFTER THE IMAGE PROCESSING #
################################################################################
    def saverCodeWriter(self):
        global g_bLive
        for x in self.outputsToSave:
            #if g_bLive:
                #self.functionCall = self.functionCall + 'cvNamedWindow("block' + self.blockNumber + '_img_o' + x +',block' + self.blockNumber + '_img_o' + x + ');\n cvShowImage("block' + self.blockNumber + '_img_o' + x +',block' + self.blockNumber + '_img_o' + x + '); \n'
            #else:
                self.functionCall = self.functionCall + 'cvSaveImage("block' + self.blockNumber + '_img_o' + x + '.png" ,block' + self.blockNumber + '_img_o' + x + ');\n'



    def create_XML_result(self, dirPathName):
        for x in self.outputsToSave:
            filename = "block" + str(self.blockNumber) + "_img_o" + x + ".png"
            im = Image.open(tmpDir + dirPathName + "/" +  filename)
            if (im.mode == 'RGB' or im.mode == 'HSV'):
                nChannels = 3 
            else:
                nChannels = 1
            depth = nChannels*8 #Provisoriamente
            self.xmlResult = '<result block=\"' + str(self.blockNumber) + '\" output=\"' + str(x) + '\">\n<content type = \"image\">\n<filename> ' + filename + '</filename>\n<properties depth=\"' + str(depth) + '\"  height= \"' + str(im.size[0]) + '\" width= \"' + str(im.size[1]) + '\"  channels=\"'+ str(nChannels) + '\" />\n</content>\n</result>'

#######################EXAMPLE OF XML_RESULT###################################
#<result block='03' output='o1'> 
#  <content type='image'>
#    <buffer>000011111101</buffer>
#    <properties depth='24' height='640'
#                width='480' channels='3' />
#  </content>
#</result>
################################################################################

def cleanTmpDir(dir):
    dirList = os.listdir(tmpDir+dir)
    for x in dirList:
        os.remove(tmpDir+dir+'/'+x)
    os.rmdir(tmpDir+dir) 

def GetErrorLog():
    if os.name == 'nt':
        Error = file(ErrorLog, 'rb')
    else:
       Error = file(ErrorLog, 'r')
    Erro = Error.read()   
    Error.close()
    return Erro

def SetErrorLog(a_sError):
    if os.name == 'nt':
        Error = file(ErrorLog, 'wb')
    else:
        Error = file(ErrorLog, 'w')
    Error.write(a_sError)
    Error.close()

from threading import Thread
class RunPrg(Thread):
	def __init__(self,cmd):
		Thread.__init__(self)
		self.cmd = cmd
	def run(self):
		os.system(self.cmd + " 2> RunErrorLog")

def parseAndGenerate(dirName, XMLChain,installDirName):
		cleanGenerator()
		global g_bSaveVideo #Passando todas as variaveis globais devolta ao default
		global g_bLive
		global g_bVideo
		global g_bCameras
		global g_bFrameRate
		global g_ShowCount
		g_ShowCount = 0
		g_bSaveVideo = []
		g_bVideo = []
		g_bCameras = []
		g_bFrameRate = 0.1
		g_bLive = False #this shall be a list containing the "blockNumbers" for each live acquisition block; len(g_bLive) works just like it is now..
		yield [_("Starting Up Generator")]
		doc = binderytools.bind_file(XMLChain)
		########################Create the blocks from XMLChain############################
		
		##################################################################################
		#				in the future we may want to show some kind of progress bar..
		#							the next few comented lines implement a progress counter.. this could be thrown up to the GUI via yields =]
		##################################################################################
		#t_nBlockCount = 0.0
		#for block in (doc.harpia.properties.block):
			#t_nBlockCount += 1.0
		#t_nItCount = 0.0
		yield [_("Generating Code")]
		for blockIter in (doc.harpia.properties.block):
				#print str(100.0*(t_nItCount/t_nBlockCount)) + "%"
				#t_nItCount += 1.0
				tmpBlock = blockTemplate()
				tmpBlock.blockType = blockIter.type
				tmpBlock.blockNumber = blockIter.id
				tmpBlock.properties = []
				tmpBlock.myConnections = []
				tmpBlock.outputsToSave = []
				try:
						for propIter in blockIter.property:
								tmpBlock.properties.append((propIter.name,propIter.value))
				except AttributeError:
						pass
				ID = tmpBlock.blockNumber
				tmpBlock.getBlockOutputTypes()
				for block in (doc.harpia.network.block):
						if (block.id == ID and int(block.type) <> 10) :
								portCount = -1
								for output in block.outputs.output:
										tmpConnection = connection()
										portCount += 1
										if output.inBlock != '--':
												tmpConnection.sourceOutput = output.id
												tmpConnection.destinationInput = output.input
												tmpConnection.destinationNumber = output.inBlock
												#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
												#!!!!!!cpscotti type-oriented connections...!!!!!
												tmpConnection.connType = tmpBlock.outTypes[int(tmpConnection.sourceOutput) - 1]
												#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
												tmpBlock.myConnections.append(tmpConnection)
										else:
												tmpConnection.destinationNumber = '--'
												tmpBlock.myConnections.append(tmpConnection)
										try:
												if output.grab == 'True':
														tmpBlock.outputsToSave.append(output.id)
										except:
												pass
		###################################################################################
		#ADDING TO EACH BLOCK OBJECT THE RESULTING CODE , THEN ADDING THE BLOCK IN A LIST #
		###################################################################################
		##Please, do not change the sequence
				tmpBlock.blockCodeWriter()
				tmpBlock.connectorCodeWriter()
				tmpBlock.saverCodeWriter()
				blockList.append(tmpBlock)
		###################################################################################

		weights = []
		#Apply the weights on each connection of each block in listOfBlocks, then return a list with its connections
		def applyWeightsOnConnections(listOfBlocks):
		#def applyWeightsOnConnections(listOfBlocks,RollinList):
				##For each block on listt:
				returnList = []
				for block in listOfBlocks:
						##Put the connections on returnList
						for connection in block.myConnections:
								##and apply the weight on this connection
								for tmpBlock in blockList:
										if tmpBlock.blockNumber == connection.destinationNumber:
												tmpBlock.weight += block.weight
												if tmpBlock not in returnList:
													#if tmpBlock not in RollinList:
													returnList.append(tmpBlock)
													#RollinList.append(tmpBlock)
				return returnList


		for block in blockList:
				#cpscotti..
				#if block.blockType == '00':
				if s2idirectory.block[int(block.blockType)]["Inputs"] == 0 and s2idirectory.block[int(block.blockType)]["Outputs"] <> 0:
						tmpList = []
						#RollinPathList = []
						tmpList.append(block)
						#RollinPathList.append(block)
						organizedChain = applyWeightsOnConnections(tmpList) #,RollinPathList)
						while organizedChain <> []:
								organizedChain = applyWeightsOnConnections(organizedChain) #,RollinPathList)
								###Recursive tests... future functionality
								#print "Start: "
								#for block in organizedChain:
									#print "\t"+str(block.blockNumber)


		biggestWeight = -1
		for block in blockList:
				if block.weight >= biggestWeight:
						biggestWeight = block.weight

		for activeWeight in range(biggestWeight):
				activeWeight += 1
				for block in blockList:
						if block.weight == activeWeight:
								arguments.append(block.functionArguments)
								images.append(block.imagesIO)
								functionCalls.append("//Weight: " + str(block.weight) + "\n")
								functionCalls.append(block.functionCall)
								deallocations.append(block.dealloc)
								outDeallocations.append(block.outDealloc)




		header = r"""// Auto-generated C Code - S2i Harpia
/*
*	In order to compile this source code run, in a terminal window, the following command:
*	gcc sourceCodeName.c `pkg-config --libs --cflags opencv` -o outputProgramName
*	
*	the `pkg-config ... opencv` parameter is a inline command that returns the path to both 
*	the libraries and the headers necessary when using opencv. The command also returns other necessary compiler options.
*/
// header:

#ifdef _CH_
#pragma package <opencv>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <opencv/cv.h>
#include <opencv/cxmisc.h>
#include <opencv/cxcore.h>
#include <opencv/ml.h>
#include <opencv/cvaux.h>
#include <opencv/cvwimage.h>
#include <opencv/highgui.h>
#include <math.h>

#define PI 3.1415926535898
double rads(double degs)
{
	return (PI/180 * degs);
}
		"""
		global usesFindSquares
		if usesFindSquares == 1:
			header += r"""

//Routines to findSquares
double angle( CvPoint* pt1, CvPoint* pt2, CvPoint* pt0 )
{
		double dx1 = pt1->x - pt0->x;
		double dy1 = pt1->y - pt0->y;
		double dx2 = pt2->x - pt0->x;
		double dy2 = pt2->y - pt0->y;
		return (dx1*dx2 + dy1*dy2)/sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10);
}

CvSeq* findSquares4( IplImage* img, CvMemStorage* storage, int minArea, int maxArea)
{
		CvSeq* contours;
		int i, c, l, N = 11;
		int thresh = 50;
		CvSize sz = cvSize( img->width & -2, img->height & -2 );
		IplImage* timg = cvCloneImage( img ); // make a copy of input image
		IplImage* gray = cvCreateImage( sz, 8, 1 ); 
		IplImage* pyr = cvCreateImage( cvSize(sz.width/2, sz.height/2), 8, 3 );
		IplImage* tgray;
		CvSeq* result;
		double s, t;

		if(minArea == -1)
			minArea = 0;
		if(maxArea == -1)
			maxArea = (img->width * img->height);

		CvSeq* squares = cvCreateSeq( 0, sizeof(CvSeq), sizeof(CvPoint), storage );
		

		cvSetImageROI( timg, cvRect( 0, 0, sz.width, sz.height ));
		
		// down-scale and upscale the image to filter out the noise
		cvPyrDown( timg, pyr, CV_GAUSSIAN_5x5 );
		cvPyrUp( pyr, timg, CV_GAUSSIAN_5x5 );
		tgray = cvCreateImage( sz, 8, 1 );
		
		// find squares in every color plane of the image
		for( c = 0; c < 3; c++ )



		{
				// extract the c-th color plane
				cvSetImageCOI( timg, c+1 );
				cvCopy( timg, tgray, 0 );
				for( l = 0; l < N; l++ )
				{
						if( l == 0 )
						{
								cvCanny( tgray, gray, 0, thresh, 5 );
								cvDilate( gray, gray, 0, 1 );
						}
						else
						{
								cvThreshold( tgray, gray, (l+1)*255/N, 255, CV_THRESH_BINARY );
						}
						cvFindContours( gray, storage, &contours, sizeof(CvContour),
								CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE, cvPoint(0,0) );
						while( contours )
						{
								result = cvApproxPoly( contours, sizeof(CvContour), storage,
										CV_POLY_APPROX_DP, cvContourPerimeter(contours)*0.02, 0 );
								if( result->total == 4 &&
										fabs(cvContourArea(result,CV_WHOLE_SEQ)) > minArea &&
										fabs(cvContourArea(result,CV_WHOLE_SEQ)) < maxArea &&
										cvCheckContourConvexity(result) )
								{
										s = 0;
										
										for( i = 0; i < 5; i++ )
										{
												if( i >= 2 )
												{
														t = fabs(angle(
														(CvPoint*)cvGetSeqElem( result, i ),
														(CvPoint*)cvGetSeqElem( result, i-2 ),
														(CvPoint*)cvGetSeqElem( result, i-1 )));
														s = s > t ? s : t;
												}
										}
										if( s < 0.3 )
												for( i = 0; i < 4; i++ )
														cvSeqPush( squares,
																(CvPoint*)cvGetSeqElem( result, i ));
								}
								contours = contours->h_next;
						}
				}
		}
		cvReleaseImage( &gray );
		cvReleaseImage( &pyr );
		cvReleaseImage( &tgray );
		cvReleaseImage( &timg );
		return squares;
}

double drawSquares( IplImage* cpy, CvSeq* squares )
{
		CvSeqReader reader;
		int i;
		cvStartReadSeq( squares, &reader, 0 );
		for( i = 0; i < squares->total; i += 4 )
		{
				CvPoint pt[4], *rect = pt;
				int count = 4;
				CV_READ_SEQ_ELEM( pt[0], reader );
				CV_READ_SEQ_ELEM( pt[1], reader );
				CV_READ_SEQ_ELEM( pt[2], reader );
				CV_READ_SEQ_ELEM( pt[3], reader );
				cvPolyLine( cpy, &rect, &count, 1, 1, CV_RGB(0,255,0), 3, CV_AA, 0 );
		}
	return (double)squares->total;
}

//End of routines to findSquares

			"""
		global usesFindColor
		if usesFindColor == 1:
			header += r"""

int GetColor(IplImage * imagem, int x, int y)
{
	return   (int)(((uchar*)(imagem->imageData + imagem->widthStep*y))[x]);
}

void SetColor(IplImage * imagem, int x, int y, uchar color)
{
	((uchar*)(imagem->imageData + imagem->widthStep*y))[x] = color;
}


void CheckImg(IplImage * img, uchar c_value, uchar tolerance)
{
	uchar min,max;
	int y_It,x_It;
	if((int)c_value < (int)tolerance)
		tolerance = c_value;

	if(((int)c_value+(int)tolerance) > 255)
		tolerance = 255 - c_value;

	min = c_value - tolerance;
	max = c_value + tolerance;

	for(y_It=0;y_It<(img->height);y_It++)
		for(x_It=0;x_It<(img->width);x_It++)
		{
				uchar val;
				val = GetColor(img,x_It,y_It);
				if(val >= min && val <= max)
					SetColor(img,x_It,y_It,255);
				else
					SetColor(img,x_It,y_It,0);
		}
}

CvPoint GetCenter(IplImage * src, long int * nOfPts)//, long int * numOfPoints)
{
	long int numOfMatchingPoints;
	long int posXsum;
	long int posYsum;
	int x_It, y_It;
	CvPoint Center;
	
	posXsum = 0;
	posYsum = 0;
	numOfMatchingPoints = 0;

	for(y_It=0;y_It<(src->height);y_It++)
		for(x_It=0;x_It<(src->width);x_It++)
			if(GetColor(src,x_It,y_It))
			{
				posXsum += x_It;
				posYsum += y_It;
				numOfMatchingPoints++;
			}

	if(numOfMatchingPoints > 0)
	{
		Center.x = (int)(posXsum/numOfMatchingPoints);
		Center.y = (int)(posYsum/numOfMatchingPoints);
	}
	else
		numOfMatchingPoints = -1;
// 	(*numOfPoints) = numOfMatchingPoints;
	if(nOfPts)
		*nOfPts = numOfMatchingPoints;

	return Center;
}


double dist22Points(CvPoint a, CvPoint b)
{
	int xD,yD;
	xD = a.x - b.x;
	yD = a.y - b.y;

	xD = (xD>0)?xD:-xD;
	yD = (yD>0)?yD:-yD;

	return (double)(xD*xD + yD*yD);
}

double GetVariance(IplImage * src,CvPoint center)//, long int * numOfPoints)
{
	long int numOfMatchingPoints;
	double distSquaresSum;
	double variance;
	int x_It,y_It;

	numOfMatchingPoints = 0;
	distSquaresSum = 0.0;


	for(y_It=0;y_It<(src->height);y_It++)
		for(x_It=0;x_It<(src->width);x_It++)
			if(GetColor(src,x_It,y_It))
			{
				numOfMatchingPoints++;
				distSquaresSum += dist22Points(center,cvPoint(x_It,y_It));
			}

	if(numOfMatchingPoints)
		variance = distSquaresSum/numOfMatchingPoints;
	else
		variance = -1;


	return variance;
}

long int CheckForColor(IplImage * src, IplImage * dst, uchar * c_value, uchar * tolerance, CvPoint * pointCenter, double * variance)
{
	uchar B,B_T,G,G_T,R,R_T;
	int i;
	long int numOfPoints;
	CvPoint centro;
	IplImage * m_pChans[3] = {NULL,NULL,NULL};

	numOfPoints = 0;

	B = c_value[0];
	G = c_value[1];
	R = c_value[2];

	B_T = tolerance[0];
	G_T = tolerance[1];
	R_T = tolerance[2];

	for(i=0;i<3;i++)
		m_pChans[i] = cvCreateImage(cvGetSize(src),IPL_DEPTH_8U, 1);

	cvSplit(src,m_pChans[0],m_pChans[1],m_pChans[2], NULL);

	CheckImg(m_pChans[0],B,B_T);
	CheckImg(m_pChans[1],G,G_T);
	CheckImg(m_pChans[2],R,R_T);

	cvAnd(m_pChans[0], m_pChans[1], dst, NULL );
	cvAnd(m_pChans[2], dst, dst, NULL );

	centro = GetCenter(dst,&numOfPoints);//,&numOfPoints);

	if(numOfPoints != -1)
		*variance = GetVariance(dst,centro);

	pointCenter->x = centro.x;
	pointCenter->y = centro.y;

	cvReleaseImage( &m_pChans[0] );
	cvReleaseImage( &m_pChans[1] );
	cvReleaseImage( &m_pChans[2] );

	return numOfPoints;
}
			"""
		header += "\nint main(int argc, char ** argv)\n{"

		declaration = "\n\t//declaration block\n"
		
		for x in arguments:
				declaration = declaration + x

		for x in images:
				declaration = declaration + x

		if g_bLive:
				declaration += \
				'int end;  end = 0; int key; \n'
				for aCapture in g_bVideo:
					declaration += 'CvCapture * block' + aCapture[0] + '_capture = NULL; \n IplImage * block' + aCapture[0] + '_frame = NULL; \n block' + aCapture[0] + '_capture = cvCreateFileCapture("'+ aCapture[1] +'"); \n'
				for aCamera in g_bCameras:
					declaration += 'CvCapture * block' + aCamera[0] + '_capture = NULL; \n IplImage * block' + aCamera[0] + '_frame = NULL; \n block' + aCamera[0] + '_capture = cvCaptureFromCAM(' + aCamera[1] + '); \n'
				declaration += 'while(!end) \n {\t \n'
				
				for aCapture in g_bVideo:
					declaration += 'cvGrabFrame (block' + aCapture[0] + '_capture); \n block' + aCapture[0] + '_frame = cvRetrieveFrame (block' + aCapture[0] + '_capture); \n'
				
				for aCamera in g_bCameras:
					declaration += 'cvGrabFrame (block' + aCamera[0] + '_capture); \n block' + aCamera[0] + '_frame = cvRetrieveFrame (block' + aCamera[0] + '_capture); \n'

		execution = "\n\t//execution block\n"
		for x in functionCalls:
				execution += x
		if g_ShowCount == 0:
			execution += '\n\tcvNamedWindow("Control Window",CV_WINDOW_AUTOSIZE );'
		if g_bLive:
				execution += '\n\tkey = cvWaitKey (' + str(int((1.0/g_bFrameRate)*1000.0)) + ');\n if(key != -1)\n end = 1;'
			
				
				deallocating = "\n\t//deallocation block\n"
				for x in deallocations:
						deallocating += x 
				
				deallocating += "}"
				
		else:
				deallocating = "\n\t//deallocation block\n"
				
				for x in deallocations:
						deallocating += x 

		closing = ""
		closing += "\n"
		for outDea in outDeallocations:
			closing += outDea
		if g_bLive:
			for aCapture in g_bVideo:
				closing += 'cvReleaseCapture(&block' + aCapture[0] + '_capture);\n'
			for aCamera in g_bCameras:
				closing += 'cvReleaseCapture(&block' + aCamera[0] + '_capture);\n'
		for vWriter in g_bSaveVideo:
			closing += 'cvReleaseVideoWriter(&block' + vWriter + '_vidWriter);\n'
		closing += "return 0;\n } //closing main()\n"
		
		
		#Final code assembly
		entireCode = header+declaration+execution+deallocating+closing
		
		yield [_("Saving Code")]
		#saving code file
		os.chdir(tmpDir+dirName)
		codeFilename = dirName + '.c'
		codeFile = open(codeFilename, 'w')
		codeFile.write(entireCode)
		codeFile.close()
		
		yield [_("Building Makefile")]
		#Assembly of "necessary" makefiles
		#...windows..
		makeFilename = 'Makefile' + dirName + '.bat'
		makeFileEntry = '"' + installDirName+'\\bin\\gcc.exe" ' + codeFilename + " -o " + codeFilename[:-2] + ".exe -lcv -lcxcore -lhighgui"
		makeFile = open(makeFilename, 'w')
		makeFile.write(makeFileEntry)
		makeFile.close()
		
		#...posix..
		makeFilename = 'Makefile.' + dirName
		makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"+installDirName+"/lib/; export PKG_CONFIG_PATH="+installDirName+"/lib/pkgconfig/;g++ "+ codeFilename +" -o " + codeFilename[:-2] + " `pkg-config --cflags --libs opencv`"
		makeFile = open(makeFilename, 'w')
		makeFile.write(makeFileEntry)
		makeFile.close()
		
		yield [_("Compiling ...")]
		if os.name=="nt":
				i,o = os.popen4('Makefile' + dirName + '.bat')

				o.readlines()
				o.close()
				i.close()
				yield [_("Running ...")]
				i,o = os.popen4(codeFilename[:-2]+'.exe')
		
		## ERROR LOG
				Error = ''
				errorList = o.readlines()
				for element in errorList:
						Error = Error + element
				
				SetErrorLog(Error)

				o.readlines()
				o.close()
				i.close()
		else:
				i,o = os.popen4("sh " + makeFilename)

				## appending compile errors too.. helps finding bugs! =]
				CompilingErrors = ''
				CerrorList = o.readlines()

				if len(CerrorList) <> 0:
					CompilingErrors += "Something was detected while compiling the source code.\n" + \
												"There is a huge chance you've found a bug, please report to scotti@das.ufsc.br \n" + \
												"sending the processing chain (.hrp), this error message and some description on what you were doing.\n" + \
												"We appreciate your help!\n"
				for element in CerrorList:
					CompilingErrors += element
				
				o.close()
				i.close()
				if g_bLive:
					yield [_("Running, press any key (on the video output window) to terminate."), CompilingErrors]
				else:
					yield [_("Running ..."), CompilingErrors]
				
				#cpscotti, xunxo bunitinho pra nao travar a interface qndo tive rodando o live =]
				t_oPrg = RunPrg("LD_LIBRARY_PATH=" + installDirName + "/lib/ ./"+codeFilename[:-2])
				t_oPrg.start()
				while t_oPrg.isAlive():
					t_oPrg.join(0.4)
					while gtk.events_pending():
						gtk.main_iteration(False)
				
				#fim do "xunx"
				
				## ERROR LOG
				o = open("RunErrorLog","r")
				Error = ''
				errorList = o.readlines()
				for element in errorList:
						Error += element
				
				yield [_("Leaving.."), Error]
				SetErrorLog(CompilingErrors + Error)

				o.close()
				i.close()
