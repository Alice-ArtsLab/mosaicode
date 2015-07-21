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
#----------------------------------------------------------------------

from classes.fill import Fill

#i18n
import gettext
APP='harpia'
DIR='/usr/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#moved down to allow changes without screwing newBlock.sh work
##HERE: ADD TYPED ICONS for inputs and outputs
#icons = {
    #"IconInput":"images/s2iinput.png",
    #"IconOutput":"images/s2ioutput.png"
    #}

#typeIconsIn = {
		#"HRP_INT":"images/s2iintin.png",
		#"HRP_IMAGE":"images/s2iinput.png"
		#}

#typeIconsOut = {
		#"HRP_INT":"images/s2iintout.png",
		#"HRP_IMAGE":"images/s2ioutput.png"
		#}

##Available groups!! PAY ATTENTION TO THIS BEFORE ADDING A NEW GROUP
#groups = {
			#_("General"):[],
			#_("Arithmetic and logical operations"):[],
			#_("Gradients, Edges and Corners"):[],
			#_("Math Functions"):[],
			#_("Filters and Color Conversion"):[],
			#_("Morphological Operations"):[],
			#_("Experimental"):[],
			#_("Feature Detection"):[],
			#_("Histograms"):[]
				#}

		
block = {
    00: {"Label":_("Image"),
         "Path":{"Python":"acquisition",
                 "Glade":"glade/acquisition.ui",
                 "Xml":"xml/acquisition.xml"},
         "Inputs":0,
         "Outputs":1,
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
				 "InTypes":"",
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Create a new image or load image from a source, such as file, camera, frame grabber."),
				 "TreeGroup":_("General"),
				 "IsSource":True #optional argument, if key doesn't exist, admit false
         },
    
    01: {"Label":_("Save Image"),
         "Path":{"Python":"save",
                 "Glade":"glade/save.ui",
                 "Xml":"xml/save.xml"} ,
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/save.png",
         "Color":"50:100:200:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Save image on a file indicated by the user."),
				 "TreeGroup":_("General")
         },

    02: {"Label":_("Show Image"),
         "Path":{"Python":"show",
                 "Glade":"glade/show.ui",
                 "Xml":"xml/show.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/show.png",
         "Color":"50:100:200:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Shows the input image on a new window."),
				 "TreeGroup":_("General")
         },

    03: {"Label":_("Histogram"),
         "Path":{"Python":"plotHistogram",
                 "Glade":"glade/plotHistogram.ui",
                 "Xml":"xml/plotHistogram.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/plotHistogram.png",
         "Color":"0:0:0:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Create a representation of the light intensity levels as an histogram."),
				 "TreeGroup":_("Histograms")
         },

    04: {"Label":_("Equalize Histogram"),
         "Path":{"Python":"equalizeHistogram",
                 "Glade":"glade/equalizeHistogram.ui",
                 "Xml":"xml/equalizeHistogram.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/equalizeHistogram.png",
         "Color":"0:0:0:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("The histogram equalization of an image intends to reinforce contrast of the image elements."),
				 "TreeGroup":_("Histograms")
         },

    06: {"Label":_("Color Conversion"),
         "Path":{"Python":"colorConversion",
                 "Glade":"glade/colorConversion.ui",
                 "Xml":"xml/colorConversion.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/colorConversion.png",
         "Color":"50:125:50:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Convert colors between different standards of graylevel/color images."),
				 "TreeGroup":_("Filters and Color Conversion")
         },

    07: {"Label":_("Compose RGB"),
         "Path":{"Python":"composeRGB",
                 "Glade":"glade/composeRGB.ui",
                 "Xml":"xml/composeRGB.xml"},
         "Inputs":3,
         "Outputs":1,
         "Icon":"images/composeRGB.png",
         "Color":"50:125:50:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE",2:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Compose three color channels  (R, G and B)  into one color image."),
				 "TreeGroup":_("Filters and Color Conversion")
         },

    8: {"Label":_("Decompose RGB"),
         "Path":{"Python":"decomposeRGB",
                 "Glade":"glade/decomposeRGB.ui",
                 "Xml":"xml/decomposeRGB.xml"},
         "Inputs":1,
         "Outputs":3,
         "Icon":"images/decomposeRGB.png",
         "Color":"50:125:50:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE",2:"HRP_IMAGE"},
				 "Description":_("Decompose a color image in three color channels (R, G and B)."),
				 "TreeGroup":_("Filters and Color Conversion")
         },
         
    9: Fill().getBlock(),

    10: {"Label":_("Comment"),
         "Path":{"Python":"comment",
                 "Glade":"glade/comment.ui",
                 "Xml":"xml/comment.xml"},
         "Inputs":0,
         "Outputs":0,
         "Icon":"images/comment.png",
         "Color":"50:100:200:150",
				 "InTypes":"",
				 "OutTypes":"",
				 "Description":_("Insert a comment."),
				 "TreeGroup":_("General")
         },

    20: {"Label":_("Sum"),
         "Path":{"Python":"sum",
                 "Glade":"glade/sum.ui",
                 "Xml":"xml/sum.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/sum.png", 
         "Color":"180:10:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Sum two images."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },

    21: {"Label":_("Subtraction"),
         "Path":{"Python":"subtraction",
                 "Glade":"glade/subtraction.ui",
                 "Xml":"xml/subtraction.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/subtraction.png",
         "Color":"180:10:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Subtract two images."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },

    22: {"Label":_("Multiplication"),
                  "Path":{"Python":"multiplication",
                 "Glade":"glade/multiplication.ui",
                 "Xml":"xml/multiplication.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/multiplication.png" ,
         "Color":"180:10:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Multiplies two images"),
				 "TreeGroup":_("Arithmetic and logical operations")
         },

    23: {"Label":_("Division"),
         "Path":{"Python":"division",
                 "Glade":"glade/division.ui",
                 "Xml":"xml/division.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/division.png",
         "Color":"180:10:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Divide two images."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },

    40: {"Label":_("Not"),
         "Path":{"Python":"not",
                 "Glade":"glade/not.ui",
                 "Xml":"xml/not.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/not.png",
         "Color":"10:180:10:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Negate the image. It is equivalent to the negative image."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },

    41: {"Label":_("And"),
         "Path":{"Python":"and",
                 "Glade":"glade/and.ui",
                 "Xml":"xml/and.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/and.png",
         "Color":"10:180:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Logical AND operation between two images."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },     
    
    42: {"Label":_("Or"),
         "Path":{"Python":"or",
                 "Glade":"glade/or.ui",
                 "Xml":"xml/or.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/or.png",
         "Color":"10:180:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Logical OR operation between two images."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },     

    43: {"Label":_("Xor"),
         "Path":{"Python":"xor",
                 "Glade":"glade/xor.ui",
                 "Xml":"xml/xor.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/xor.png",
         "Color":"10:180:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Logical XOR (exclusive-or) operation between two images."),
				 "TreeGroup":_("Arithmetic and logical operations")
         },     

    60: {"Label":_("Pow"),
         "Path":{"Python":"pow",
                 "Glade":"glade/pow.ui",
                 "Xml":"xml/pow.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/pow.png",
         "Color":"230:230:60:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Power each pixel value to a fixed value."),
				 "TreeGroup":_("Math Functions")
         },     

    61: {"Label":_("Exp"),
         "Path":{"Python":"exp",
                 "Glade":"glade/exp.ui",
                 "Xml":"xml/exp.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/exp.png",
         "Color":"230:230:60:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Return the image made from the neperian constant (e) powered to each one of the image pixels."),
				 "TreeGroup":_("Math Functions")
         },     

    62: {"Label":_("Log"),
         "Path":{"Python":"log",
                 "Glade":"glade/log.ui",
                 "Xml":"xml/log.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/log.png",
         "Color":"230:230:60:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Return the image made from the neperian logarithm of each one of the image pixels."),
				 "TreeGroup":_("Math Functions")
         },     

    80: {"Label":_("Sobel"),
         "Path":{"Python":"sobel",
                 "Glade":"glade/sobel.ui",
                 "Xml":"xml/sobel.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/sobel.png",
         "Color":"250:180:80:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Filtering operation that uses the Sobel mask to enhance edges on the image."),
				 "TreeGroup":_("Gradients, Edges and Corners")
         },     

    81: {"Label":_("Laplace"),
         "Path":{"Python":"laplace",
                 "Glade":"glade/laplace.ui",
                 "Xml":"xml/laplace.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/laplace.png",
         "Color":"250:180:80:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Filtering operation that uses the Laplacian mask to enhance edges on the image."),
				 "TreeGroup":_("Gradients, Edges and Corners")
         },     

    82: {"Label":_("Smooth"),
         "Path":{"Python":"smooth",
                 "Glade":"glade/smooth.ui",
                 "Xml":"xml/smooth.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/smooth.png",
         "Color":"50:125:50:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Filtering operation that smooths the image."),
				 "TreeGroup":_("Filters and Color Conversion")
         },     

    83: {"Label":_("Canny"),
         "Path":{"Python":"canny",
                 "Glade":"glade/canny.ui",
                 "Xml":"xml/canny.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/canny.png",
         "Color":"250:180:80:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Filtering operation that employs the Canny algorithm to detect edges."),
				 "TreeGroup":_("Gradients, Edges and Corners")
         },     

    100: {"Label":_("Erosion"),
          "Path":{"Python":"erode",
                  "Glade":"glade/erode.ui",
                  "Xml":"xml/erode.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/erode.png",
         "Color":"180:230:220:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Morphological operation that erodes the objects of the image, reducing their size."),
				 "TreeGroup":_("Morphological Operations")
         },

    101: {"Label":_("Dilate"),
          "Path":{"Python":"dilate",
                  "Glade":"glade/dilate.ui",
                  "Xml":"xml/dilate.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/dilate.png",
         "Color":"180:230:220:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Morphological operation that dilates the objects of the image, enlarging their size."),
				 "TreeGroup":_("Morphological Operations")
         },     

    102: {"Label":_("Opening"),
          "Path":{"Python":"opening",
                  "Glade":"glade/opening.ui",
                 "Xml":"xml/opening.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/opening.png",
         "Color":"180:230:220:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Morphological operation that disconnects objects and reduces noise."),
				 "TreeGroup":_("Morphological Operations")
         },     

    103: {"Label":_("Closing"),
          "Path":{"Python":"closing",
                  "Glade":"glade/closing.ui",
                  "Xml":"xml/closing.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/closing.png",
         "Color":"180:230:220:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Morphological operation that connects objects on an image."),
				 "TreeGroup":_("Morphological Operations")
          },     
    
    120: {"Label":_("Threshold"),
          "Path":{"Python":"threshold",
                  "Glade":"glade/threshold.ui",
                  "Xml":"xml/threshold.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/threshold.png",
         "Color":"50:125:50:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Image binarization operator, according to a fixed threshold value."),
				 "TreeGroup":_("Filters and Color Conversion")
          },     

    601: {"Label":_("Run Command"),
         "Path":{"Python":"runCmd",
                 "Glade":"glade/runCmd.ui",
                 "Xml":"xml/runCmd.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/runCmd.png",
         "Color":"200:200:60:150",
				 "InTypes":{0:"HRP_DOUBLE"},
				 "OutTypes":{0:"HRP_DOUBLE"},
				 "Description":_("Runs a shell command depending on the input value."),
				 "TreeGroup":_("Experimental")
         },
				 
		602: {"Label":_("Detect Hough Circles"),
         "Path":{"Python":"checkCir",
                 "Glade":"glade/checkCir.ui",
                 "Xml":"xml/checkCir.xml"},
         "Inputs":1,
         "Outputs":2,
         "Icon":"images/checkCir.png",
         "Color":"20:20:60:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_DOUBLE",1:"HRP_IMAGE"},
				 "Description":_("Output1: Returns 1 if the desired circle was found, 0 otherwise.\n Output2: The input image with the detected circles red-tagged"),
				 "TreeGroup":_("Feature Detection")
         },
		603: {"Label":_("Detect Hough Lines"),
         "Path":{"Python":"checkLin",
                 "Glade":"glade/checkLin.ui",
                 "Xml":"xml/checkLin.xml"},
         "Inputs":1,
         "Outputs":2,
         "Icon":"images/checkLin.png",
         "Color":"80:20:130:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_DOUBLE",1:"HRP_IMAGE"},
				 "Description":_("Output1: Returns 1 if the desired line was found, 0 otherwise.\n Output2: The input image with the detected lines red-tagged"),
				 "TreeGroup":_("Feature Detection")
         },
		604: {"Label":_("Resize Image"),
         "Path":{"Python":"resize",
                 "Glade":"glade/resize.ui",
                 "Xml":"xml/resize.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/resize.png",
         "Color":"20:80:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_RECT"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Resizes the input image to the dimensions of the input rectangle"),
				 "TreeGroup":_("Experimental")
         },
		605: {"Label":_("Match Template"),
         "Path":{"Python":"matchTem",
                 "Glade":"glade/matchTem.ui",
                 "Xml":"xml/matchTem.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/matchTem.png",
         "Color":"180:180:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Output shows the matching relation between image (input1) and template (input2)"),
				 "TreeGroup":_("Feature Detection")
         },
		606: {"Label":_("Find Min or Max"),
         "Path":{"Python":"minMax",
                 "Glade":"glade/minMax.ui",
                 "Xml":"xml/minMax.xml"},
         "Inputs":1,
         "Outputs":2,
         "Icon":"images/minMax.png",
         "Color":"50:50:200:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_DOUBLE",1:"HRP_POINT"},
				 "Description":_("Finds min or max from input image and judges it according to a custom criteria."),
				 "TreeGroup":_("Feature Detection")
         },
		12: {'Label':_('Live Delay'),
         'Path':{'Python':'liveDelay',
                 'Glade':'glade/liveDelay.ui',
                 'Xml':'xml/liveDelay.xml'},
         'Inputs':1,
         'Outputs':1,
         'Icon':'images/liveDelay.png',
         'Color':'250:20:30:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:'HRP_IMAGE'},
				 'Description':_('Inserts a delay inside a live stream'),
				 'TreeGroup':_('General'),
				 'TimeShifts':True
         },
		13: {'Label':_('Get Size'),
         'Path':{'Python':'getSize',
                 'Glade':'glade/getSize.ui',
                 'Xml':'xml/getSize.xml'},
         'Inputs':1,
         'Outputs':1,
         'Icon':'images/getSize.xpm',
         'Color':'250:20:30:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:'HRP_RECT'},
				 'Description':_('Extracts the input image size'),
				 'TreeGroup':_('Experimental'),
				 'TimeShifts':False
         },
    14: {"Label":_("Fill Rectangle"),
         "Path":{"Python":"fillRect",
                 "Glade":"glade/fillRect.ui",
                 "Xml":"xml/fillRect.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/fill.png",
         "Color":"50:100:200:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_RECT"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Fill the input rectangle on the input image with the desired color."),
				 "TreeGroup":_("General")
         },
		611: {'Label':_('Stereo Correspondence'),
         'Path':{'Python':'stereoCorr',
                 'Glade':'glade/stereoCorr.ui',
                 'Xml':'xml/stereoCorr.xml'},
         'Inputs':2,
         'Outputs':1,
         'Icon':'images/stereoCorr.png',
         'Color':'10:10:20:150',
				 'InTypes':{0:'HRP_IMAGE',1:"HRP_IMAGE"},
				 'OutTypes':{0:'HRP_IMAGE'},
				 'Description':_('Input1 is the left image and Input2 is the right image. Output is the depth image'),
				 'TreeGroup':_('Feature Detection')
         },
		11: {'Label':_('Save Video'),
         'Path':{'Python':'saveVideo',
                 'Glade':'glade/saveVideo.ui',
                 'Xml':'xml/saveVideo.xml'},
         'Inputs':1,
         'Outputs':1,
         'Icon':'images/saveVideo.png',
         'Color':'120:20:20:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:'HRP_IMAGE'},
				 'Description':_('Save Video needs its description'),
				 'TreeGroup':_('General')
         },
		610: {'Label':_('Haar (face) Detector'),
         'Path':{'Python':'haarDetect',
                 'Glade':'glade/haarDetect.ui',
                 'Xml':'xml/haarDetect.xml'},
         'Inputs':1,
         'Outputs':4,
         'Icon':'images/haarDetect.png',
         'Color':'50:220:40:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:'HRP_POINT',1:'HRP_RECT',2:'HRP_IMAGE',3:'HRP_DOUBLE'},
				 'Description':_('Haar (face) Detector finds regions on the input image according to the given haar-classifier. \n First Output is the center of the first \
detected feature, second is a rectangle around the first detected feature and the third is the input image with the detected features tagged by a red circle.\n \
The last output is the number of detected faces.'),
				 'TreeGroup':_("Feature Detection")
         },
		609: {'Label':_('Find object of a given color'),
         'Path':{'Python':'findColor',
                 'Glade':'glade/findColor.ui',
                 'Xml':'xml/findColor.xml'},
         'Inputs':1,
         'Outputs':4,
         'Icon':'images/findColor.png',
         'Color':'50:50:200:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:"HRP_POINT",1:"HRP_DOUBLE",2:"HRP_DOUBLE",3:"HRP_IMAGE"},
				 'Description':_('Find object of a given color and points its center\n Output 1 = Center Point\n Output2 = Number of matching points\n Output3 = Variance \n Output4 = Tagged Image'),
				 'TreeGroup':_('Feature Detection')
         },
		608: {'Label':_('Find Squares'),
         'Path':{'Python':'findSquares',
                 'Glade':'glade/findSquares.ui',
                 'Xml':'xml/findSquares.xml'},
         'Inputs':1,
         'Outputs':2,
         'Icon':'images/findSquares.png',
         'Color':'50:50:200:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:"HRP_DOUBLE",1:"HRP_IMAGE"},
				 'Description':_('Finds four-sided polygons on the input image.\n Output 1 = Number of detected Polygons\n Output 2 = The input image tagged with the found polygons.'),
				 'TreeGroup':_('Feature Detection')
         },
		803: {'Label':_('Move Rectangle'),
         'Path':{'Python':'moveRct',
                 'Glade':'glade/moveRct.ui',
                 'Xml':'xml/moveRct.xml'},
         'Inputs':2,
         'Outputs':1,
         'Icon':'images/moveRct.png',
         'Color':'50:50:200:150',
				 'InTypes':{0:'HRP_RECT',1:'HRP_POINT'},
				 'OutTypes':{0:'HRP_RECT'},
				 'Description':_('Move Rectangle`s (0,0) point to input point'),
				 'TreeGroup':_('Experimental')
         },
		902: {'Label':_('Check Point'),
         'Path':{'Python':'isOnRect',
                 'Glade':'glade/isOnRect.ui',
                 'Xml':'xml/isOnRect.xml'},
         'Inputs':2,
         'Outputs':1,
         'Icon':'images/isOnRect.png',
         'Color':'50:50:200:150',
				 'InTypes':{0:'HRP_POINT',1:'HRP_RECT'},
				 'OutTypes':{0:'HRP_DOUBLE'},
				 'Description':_('Checks Wheather the given point is inside the given rectangle'),
				 'TreeGroup':_('Experimental')
         },
		901: {'Label':_('New Point'),
         'Path':{'Python':'newPoint',
                 'Glade':'glade/newPoint.ui',
                 'Xml':'xml/newPoint.xml'},
         'Inputs':0,
         'Outputs':1,
         'Icon':'images/newPoint.png',
         'Color':'50:50:200:150',
				 'InTypes':"",
				 'OutTypes':{0:'HRP_POINT'},
				 'Description':_('Creates a new Point'),
				 'TreeGroup':_('Experimental'),
				 "IsSource":True
         },
		802: {'Label':_('Crop Image'),
         'Path':{'Python':'cropImage',
                 'Glade':'glade/cropImage.ui',
                 'Xml':'xml/cropImage.xml'},
         'Inputs':2,
         'Outputs':1,
         'Icon':'images/cropImage.png',
         'Color':'50:50:200:150',
				 'InTypes':{0:'HRP_IMAGE',1:'HRP_RECT'},
				 'OutTypes':{0:'HRP_IMAGE'},
				 'Description':_('Crops the input image according to input Rectangle'),
				 'TreeGroup':_('Experimental')
         },
		801: {'Label':_('New Rectangle'),
         'Path':{'Python':'newRect',
                 'Glade':'glade/newRect.ui',
                 'Xml':'xml/newRect.xml'},
         'Inputs':0,
         'Outputs':1,
         'Icon':'images/newRect.png',
         'Color':'50:50:200:150',
				 'InTypes':"",
				 'OutTypes':{0:'HRP_RECT'},
				 'Description':_('Creates new rectangle'),
				 'TreeGroup':_('Experimental'),
				 "IsSource":True
         },
		701: {'Label':_('New Double'),
         'Path':{'Python':'newDouble',
                 'Glade':'glade/newDouble.ui',
                 'Xml':'xml/newDouble.xml'},
         'Inputs':0,
         'Outputs':1,
         'Icon':'images/newDouble.png',
         'Color':'50:50:200:150',
				 'InTypes':"",
				 'OutTypes':{0:'HRP_DOUBLE'},
				 'Description':_('Creates new literal value (Double)'),
				 'TreeGroup':_('Experimental'),
				 "IsSource":True
         },
		607: {"Label":_("Rotate Image"),
         "Path":{"Python":"rotate",
                 "Glade":"glade/rotate.ui",
                 "Xml":"xml/rotate.xml"},
         "Inputs":2,
         "Outputs":1,
         "Icon":"images/rotate.png",
         "Color":"90:5:10:150",
				 "InTypes":{0:"HRP_IMAGE",1:"HRP_DOUBLE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Rotates input image the input angle degrees. (More options inside)"),
				 "TreeGroup":_("Experimental")
         }
}


#HERE: ADD TYPED ICONS for inputs and outputs
icons = {
    "IconInput":"images/s2iinput.png",
    "IconOutput":"images/s2ioutput.png"
    }

typeIconsIn = {
		"HRP_INT":"images/s2iintin.png",
		"HRP_DOUBLE":"images/s2idoubin.png",
		"HRP_RECT":"images/s2irctin.png",
		"HRP_IMAGE":"images/s2iinput.png",
		"HRP_POINT":"images/s2ipointin.png",
		"HRP_32_IMG":"images/s2i64in.png"
		}

typeIconsOut = {
		"HRP_INT":"images/s2iintout.png",
		"HRP_DOUBLE":"images/s2idoubout.png",
		"HRP_RECT":"images/s2irctout.png",
		"HRP_IMAGE":"images/s2ioutput.png",
		"HRP_POINT":"images/s2ipointout.png",
		"HRP_32_IMG":"images/s2i64out.png"
		}

#Available groups!! PAY ATTENTION TO THIS BEFORE ADDING A NEW GROUP
groups = {
			_("General"):[],
			_("Arithmetic and logical operations"):[],
			_("Gradients, Edges and Corners"):[],
			_("Math Functions"):[],
			_("Filters and Color Conversion"):[],
			_("Morphological Operations"):[],
			_("Experimental"):[],
			_("Feature Detection"):[],
			_("Histograms"):[]
				}
