# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
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

import gtk

from harpia.GladeWindow import GladeWindow
from harpia.s2icommonproperties import S2iCommonProperties, APP, DIR

# i18n
import os
from harpia.utils.XMLUtils import XMLParser
import gettext

_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

# ----------------------------------------------------------------------

class Properties(GladeWindow, S2iCommonProperties):
    # ----------------------------------------------------------------------

    def __init__(self, PropertiesXML, S2iBlockProperties):

        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']

        filename = self.m_sDataDir + 'glade/findColor.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            '_R',
            '_G',
            '_B',
            '_R_T',
            '_G_T',
            '_B_T',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'prop_confirm'
        ]

        handlers = [
            'on_cancel_clicked',
            'on_prop_confirm_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        # load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        for Property in self.block_properties:
            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "_R":
                self.widgets['_R'].set_value(float(value));
            if name == "_G":
                self.widgets['_G'].set_value(float(value));
            if name == "_B":
                self.widgets['_B'].set_value(float(value));
            if name == "_R_T":
                self.widgets['_R_T'].set_value(float(value));
            if name == "_G_T":
                self.widgets['_G_T'].set_value(float(value));
            if name == "_B_T":
                self.widgets['_B_T'].set_value(float(value));

                # if Property.name == "isFilling":
                # if Property.value == "true":
                # self.widgets['isFilling'].set_active( True );
                # else:
                # self.widgets['isFilling'].set_active( False );

                # if Property.name == "isScalling":
                # if Property.value == "true":
                # self.widgets['isScalling'].set_active( True );
                # else:
                # self.widgets['isScalling'].set_active( False );

                # if Property.name == "isCenter":
                # if Property.value == "true":
                # self.widgets['isAtCenter'].set_active( True );
                # else:
                # self.widgets['isAtPoint'].set_active( True );

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + 'help/findColor' + _('_en.help'))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def getHelp(self):
        return "Detecta formas circulares na imagem de entrada.\
        Saida 1 é a resposta da avaliacao(*) e a saida dois mostra \
        os circulos encontrados."
    #-----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        self.widgets['prop_confirm'].grab_focus()
        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "_R":
                Property.setAttr("value", unicode(self.widgets['_R'].get_value()))
            if name == "_G":
                Property.setAttr("value", unicode(self.widgets['_G'].get_value()))
            if name == "_B":
                Property.setAttr("value", unicode(self.widgets['_B'].get_value()))
            if name == "_R_T":
                Property.setAttr("value", unicode(self.widgets['_R_T'].get_value()))
            if name == "_G_T":
                Property.setAttr("value", unicode(self.widgets['_G_T'].get_value()))
            if name == "_B_T":
                Property.setAttr("value", unicode(self.widgets['_B_T'].get_value()))

                # if Property.name == "isCenter":
                # if self.widgets['isAtCenter'].get_active():
                # Property.value = u"true"
                # else:
                # Property.value = u"false"

                # if Property.name == "isFilling":
                # if self.widgets['isFilling'].get_active():
                # Property.value = u"true"
                # else:
                # Property.value = u"false"

                # if Property.name == "isScalling":
                # if self.widgets['isScalling'].get_active():
                # Property.value = u"true"
                # else:
                # Property.value = u"false"

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)
        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)
        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------


# propProperties = Properties()()
# propProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    blockTemplate.header += r"""

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
    for propIter in blockTemplate.properties:
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

    # o1 - pto
    # o2 - numOfPoints
    # o3 - variance
    # o4 - img
    blockTemplate.imagesIO = \
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'IplImage * block$$_img_o4 = NULL;\n' + \
        'CvPoint block$$_point_o1;\n' + \
        'uchar block$$c_value[3] = {' + c_B + ',' + c_G + ',' + c_R + '};\n' + \
        'uchar block$$tolerance[3] = {' + c_B_T + ',' + c_G_T + ',' + c_R_T + '};\n' + \
        'double block$$_double_o2;\n' + \
        'double block$$_double_o3;\n'
    blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                 '	IplImage * block$$_img_t1 = cvCreateImage(cvGetSize(block$$_img_i1),IPL_DEPTH_8U, 1);\n' + \
                                 '	if(!block$$_img_o4)\n' + \
                                 '		block$$_img_o4 = cvCloneImage(block$$_img_i1);\n' + \
                                 '	else\n' + \
                                 ' 	cvCopy(block$$_img_i1,block$$_img_o4,0);\n' + \
                                 '	block$$_double_o2 = CheckForColor(block$$_img_i1, block$$_img_t1, block$$c_value, block$$tolerance, &block$$_point_o1, &block$$_double_o3);\n' + \
                                 '	cvCircle(block$$_img_o4,block$$_point_o1,8,cvScalarAll(255),4,8,0);\n' + \
                                 '	cvReleaseImage(&block$$_img_t1);\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o4);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Find object of a given color'),
            'Path': {'Python': 'findColor',
                     'Glade': 'glade/findColor.ui',
                     'Xml': 'xml/findColor.xml'},
            'Icon': 'images/findColor.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: "HRP_POINT", 1: "HRP_DOUBLE", 2: "HRP_DOUBLE", 3: "HRP_IMAGE"},
            'Description': _(
                'Find object of a given color and points its center\n Output 1 = Center Point\n Output2 = Number of matching points\n Output3 = Variance \n Output4 = Tagged Image'),
            'TreeGroup': _('Feature Detection')
            }
