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

import bpGUI
#from harpia.bpGUI import *
from harpia.constants import *

import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


block = {
        01: {"Label":_("Luan"),
         "Path":{"Python":"acquisition",
                 "Glade":"glade/acquisition.ui",
                 "Xml":"xml/acquisition.xml"},
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":{0:"HRP_IMAGE", 1:"HRP_IMAGE"},
                 "OutTypes":{0:"HRP_IMAGE", 1:"HRP_IMAGE", 2:"HRP_IMAGE"},
                 "Description":_("Create a new image or load image from a source, such as file, camera, frame grabber."),
                 "TreeGroup":_("General"),
                 "IsSource":True #optional argument, if key doesn't exist, admit false
         }
#        01: save.getBlock(),
#        02: show.getBlock(),
#        03: plotHistogram.getBlock(),
#        04: equalizeHistogram.getBlock(),
#        06: colorConversion.getBlock(),
#        07: composeRGB.getBlock(),
#        8: decomposeRGB.getBlock(),
#        9: fill.getBlock(),
#        10: comment.getBlock(),
#        11: saveVideo.getBlock(),
#        12: liveDelay.getBlock(),
#        13: getSize.getBlock(),
#        14: fillRect.getBlock(),
#        20: Sum.getBlock(),
#        21: subtraction.getBlock(),
#        22: multiplication.getBlock(),
#        23: division.getBlock(),
#        40: Not.getBlock(),
#        41: And.getBlock(),     
#        42: Or.getBlock(),     
#        43: xor.getBlock(),     
#        60: Pow.getBlock(),     
#        61: exp.getBlock(),     
#        62: log.getBlock(),
#        80: sobel.getBlock(),     
#        81: laplace.getBlock(),     
#        82: smooth.getBlock(),     
#        83: canny.getBlock(),
#        100: erode.getBlock(),
#        101: dilate.getBlock(),
#        102: opening.getBlock(),
#        103: closing.getBlock(),
#        120: threshold.getBlock(),
#        601: runCmd.getBlock(),
#        602: checkCir.getBlock(),
#        603: checkLin.getBlock(),
#        604: resize.getBlock(),
#        605: matchTem.getBlock(),
#        606: minMax.getBlock(),
#        607: rotate.getBlock(),
#        608: findSquares.getBlock(),
#        609: findColor.getBlock(),
#        610: haarDetect.getBlock(),
#        611: stereoCorr.getBlock(),
#        701: newDouble.getBlock(),
#        801: newRect.getBlock(),
#        802: cropImage.getBlock(),
#        803: moveRct.getBlock(),
#        901: newPoint.getBlock(),
#        902: isOnRect.getBlock()
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
            _("Basic Data Type"):[],
            _("Arithmetic and logical operations"):[],
            _("Gradients, Edges and Corners"):[],
            _("Math Functions"):[],
            _("Filters and Color Conversion"):[],
            _("Morphological Operations"):[],
            _("Experimental"):[],
            _("Feature Detection"):[],
            _("Histograms"):[]
                }
