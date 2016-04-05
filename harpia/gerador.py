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
# ----------------------------------------------------------------------

################################WARNING!!###########################################
#                      DO NOT MANUALLY EDIT THIS FILE                              #
# LET THE MODIFICATIONS BE INSERTED BY THE TOOLS PROVIDED WITH HARPIA SYSTEM       #
####################################################################################

#############################INCLUDES AND DECLARATIONS##############################
import os
import gtk

####################################INCLUDES OF CLASS##########################################

from connection import connection
from blockTemplate import blockTemplate
from RunPrg import RunPrg


###############################################################################################
# from popen2 import Popen4

from bpGUI import *
from harpia.utils.XMLUtils import XMLParser
from constants import *

# i18n
import gettext
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

if os.name == "nt":
    tmpDir = os.path.join(os.path.expanduser("~"), "tmp\\")
    if not (os.path.exists(tmpDir)):
        os.makedirs(tmpDir, mode=0700)
else:
    tmpDir = "/tmp/"


def __clean_generator():
    global arguments, images, functionCalls, deallocations, outDeallocations, blockList
    arguments = []
    images = []
    functionCalls = []
    deallocations = []
    outDeallocations = []
    blockList = []


# Global variable to indicate overall behavior of the code generator

g_bLive = False  # default eh live!!

g_ShowCount = 0

g_bCameras = []
g_bVideo = []  # default eh live!!
g_bSaveVideo = []

g_bFrameRate = 0.1

g_sCaptureLive = '0'
g_sVideoFilename = ''
# g_flagFrame = 1

usesFindSquares = 0
usesFindColor = 0


####################################################################################

######################### input images with different sizes must be treated ########

def inputSizeComply(nInputs, currentBlockN):
    if nInputs == 2:
        outPutCode = 'if(block' + str(currentBlockN) + '_img_i1->width != block' + str(
            currentBlockN) + '_img_i2->width || ' + \
                     'block' + str(currentBlockN) + '_img_i1->height != block' + str(
            currentBlockN) + '_img_i2->height)\n{\n' + \
                     '	int minW,minH;\n' + \
                     '	if(block' + str(currentBlockN) + '_img_i1->width > block' + str(
            currentBlockN) + '_img_i2->width)\n' + \
                     '		minW = block' + str(currentBlockN) + '_img_i2->width;\n' + \
                     '	else \n' + \
                     '		minW = block' + str(currentBlockN) + '_img_i1->width;\n\n' + \
                     '	if(block' + str(currentBlockN) + '_img_i1->height > block' + str(
            currentBlockN) + '_img_i2->height)\n' + \
                     '		minH = block' + str(currentBlockN) + '_img_i2->height;\n' + \
                     '	else \n' + \
                     '		minH = block' + str(currentBlockN) + '_img_i1->height;\n\n' + \
                     '	cvSetImageROI(block' + str(currentBlockN) + '_img_i2, cvRect( 0, 0, minW, minH ));\n' + \
                     '	cvSetImageROI(block' + str(currentBlockN) + '_img_i1, cvRect( 0, 0, minW, minH ));\n' + \
                     '	cvSetImageROI(block' + str(currentBlockN) + '_img_o1, cvRect( 0, 0, minW, minH ));\n' + \
                     '}\n'
        return (outPutCode)
    else:
        return ("//Image Sizes match\n")


def __set_error_log(a_sError):
    if os.name == 'nt':
        Error = file(ErrorLog, 'wb')
    else:
        Error = file(ErrorLog, 'w')
    Error.write(a_sError)
    Error.close()

def parseAndGenerate(dirName, XMLChain, installDirName):
    __clean_generator()
    global g_bSaveVideo  # Passando todas as variaveis globais devolta ao default
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
    g_bLive = False  # this shall be a list containing the "blockNumbers" for each live acquisition block; len(g_bLive) works just like it is now..
    yield [_("Starting Up Generator")]
    #doc = binderytools.bind_file(XMLChain)
    doc = XMLParser(XMLChain)
    ########################Create the blocks from XMLChain############################

    ##################################################################################
    #				in the future we may want to show some kind of progress bar..
    #							the next few comented lines implement a progress counter.. this could be thrown up to the GUI via yields =]
    ##################################################################################
    # t_nBlockCount = 0.0
    # for block in (doc.harpia.properties.block):
    # t_nBlockCount += 1.0
    # t_nItCount = 0.0
    yield [_("Generating Code")]
    blocks = doc.getTag("harpia").getTag("properties").getChildTags("block")
    for blockIter in blocks:
        # print str(100.0*(t_nItCount/t_nBlockCount)) + "%"
        # t_nItCount += 1.0
        tmpBlock = blockTemplate()
        tmpBlock.blockType = blockIter.type
        tmpBlock.blockNumber = blockIter.id
        tmpBlock.properties = []
        tmpBlock.myConnections = []
        tmpBlock.outputsToSave = []
        try:
            block_properties = blockIter.getChildTags("property")
            for propIter in block_properties:
                tmpBlock.properties.append((propIter.name, propIter.value))
        except AttributeError:
            pass
        ID = tmpBlock.blockNumber
        tmpBlock.getBlockOutputTypes()

        net_blocks = doc.getTag("harpia").getTag("network").getChildTags("block")
        for block in net_blocks:
            if (block.id == ID and int(block.type) <> 10):
                portCount = -1
                outputs = block.getTag("outputs").getChildTags("output")
                for output in outputs:
                    tmpConnection = connection()
                    portCount += 1
                    if output.inBlock != '--':
                        tmpConnection.sourceOutput = output.id
                        tmpConnection.destinationInput = output.input
                        tmpConnection.destinationNumber = output.inBlock
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!cpscotti type-oriented connections...!!!!!
                        tmpConnection.connType = tmpBlock.outTypes[int(tmpConnection.sourceOutput) - 1]
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
                    # ADDING TO EACH BLOCK OBJECT THE RESULTING CODE , THEN ADDING THE BLOCK IN A LIST #
                    ###################################################################################
                    ##Please, do not change the sequence
        tmpBlock.blockCodeWriter()
        tmpBlock.connectorCodeWriter()
        tmpBlock.saverCodeWriter()
        blockList.append(tmpBlock)
    ###################################################################################

    weights = []
    # Apply the weights on each connection of each block in listOfBlocks, then return a list with its connections
    def applyWeightsOnConnections(listOfBlocks):
        # def applyWeightsOnConnections(listOfBlocks,RollinList):
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
                            # if tmpBlock not in RollinList:
                            returnList.append(tmpBlock)
                        # RollinList.append(tmpBlock)
        return returnList

    for block in blockList:
        # cpscotti..
        # if block.blockType == '00':
        if len(s2idirectory.block[int(block.blockType)]["InTypes"]) == 0 and len(s2idirectory.block[int(block.blockType)]["OutTypes"]) <> 0:
            tmpList = []
            # RollinPathList = []
            tmpList.append(block)
            # RollinPathList.append(block)
            organizedChain = applyWeightsOnConnections(tmpList)  # ,RollinPathList)
            while organizedChain <> []:
                organizedChain = applyWeightsOnConnections(organizedChain)  # ,RollinPathList)
            ###Recursive tests... future functionality
            # print "Start: "
            # for block in organizedChain:
            # print "\t"+str(block.blockNumber)

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
            declaration += 'CvCapture * block' + aCapture[0] + '_capture = NULL; \n IplImage * block' + aCapture[
                0] + '_frame = NULL; \n block' + aCapture[0] + '_capture = cvCreateFileCapture("' + aCapture[
                               1] + '"); \n'
        for aCamera in g_bCameras:
            declaration += 'CvCapture * block' + aCamera[0] + '_capture = NULL; \n IplImage * block' + aCamera[
                0] + '_frame = NULL; \n block' + aCamera[0] + '_capture = cvCaptureFromCAM(' + aCamera[1] + '); \n'
        declaration += 'while(!end) \n {\t \n'

        for aCapture in g_bVideo:
            declaration += 'cvGrabFrame (block' + aCapture[0] + '_capture); \n block' + aCapture[
                0] + '_frame = cvRetrieveFrame (block' + aCapture[0] + '_capture); \n'

        for aCamera in g_bCameras:
            declaration += 'cvGrabFrame (block' + aCamera[0] + '_capture); \n block' + aCamera[
                0] + '_frame = cvRetrieveFrame (block' + aCamera[0] + '_capture); \n'

    execution = "\n\t//execution block\n"
    for x in functionCalls:
        execution += x
    if g_ShowCount == 0:
        execution += '\n\tcvNamedWindow("Control Window",CV_WINDOW_AUTOSIZE );'
    if g_bLive:
        execution += '\n\tkey = cvWaitKey (' + str(int((1.0 / g_bFrameRate) * 1000.0)) + ');\n if(key != -1)\n end = 1;'

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


    # Final code assembly
    entireCode = header + declaration + execution + deallocating + closing

    yield [_("Saving Code")]
    # saving code file
    os.chdir(tmpDir + dirName)
    codeFilename = dirName + '.c'
    codeFile = open(codeFilename, 'w')
    codeFile.write(entireCode)
    codeFile.close()

    yield [_("Building Makefile")]
    # Assembly of "necessary" makefiles
    # ...windows..
    makeFilename = 'Makefile' + dirName + '.bat'
    makeFileEntry = '"' + installDirName + '\\bin\\gcc.exe" ' + codeFilename + " -o " + codeFilename[
                                                                                        :-2] + ".exe -lcv -lcxcore -lhighgui"
    makeFile = open(makeFilename, 'w')
    makeFile.write(makeFileEntry)
    makeFile.close()

    # ...posix..
    makeFilename = 'Makefile.' + dirName
    makeFileEntry = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:" + installDirName + "/lib/; export PKG_CONFIG_PATH=" + installDirName + "/lib/pkgconfig/;g++ " + codeFilename + " -o " + codeFilename[
                                                                                                                                                                                       :-2] + " `pkg-config --cflags --libs opencv`"
    makeFile = open(makeFilename, 'w')
    makeFile.write(makeFileEntry)
    makeFile.close()

    yield [_("Compiling ...")]
    if os.name == "nt":
        i, o = os.popen4('Makefile' + dirName + '.bat')

        o.readlines()
        o.close()
        i.close()
        yield [_("Running ...")]
        i, o = os.popen4(codeFilename[:-2] + '.exe')

        ## ERROR LOG
        Error = ''
        errorList = o.readlines()
        for element in errorList:
            Error = Error + element

        __set_error_log(Error)

        o.readlines()
        o.close()
        i.close()
    else:
        i, o = os.popen4("sh " + makeFilename)

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

        # cpscotti, xunxo bunitinho pra nao travar a interface qndo tive rodando o live =]
        t_oPrg = RunPrg("LD_LIBRARY_PATH=" + installDirName + "/lib/ ./" + codeFilename[:-2])
        t_oPrg.start()
        while t_oPrg.isAlive():
            t_oPrg.join(0.4)
            while gtk.events_pending():
                gtk.main_iteration(False)

        # fim do "xunx"

        ## ERROR LOG
        o = open("RunErrorLog", "r")
        Error = ''
        errorList = o.readlines()
        for element in errorList:
            Error += element

        yield [_("Leaving.."), Error]
        __set_error_log(CompilingErrors + Error)

        o.close()
        i.close()
