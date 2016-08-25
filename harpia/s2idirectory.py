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

import harpia.plugins
from harpia.constants import *
from harpia.control.harpiapropertiescontrol import *
from harpia.model.harpiaproperties import *

import pkgutil # For dynamic package load
import inspect # For module inspect

from glob import glob # To load examples
import os
import copy

import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

Log = None

properties = HarpiaProperties()

block = {}
list_of_examples = []
recent_files = []

def load():
    for importer, modname, ispkg in pkgutil.iter_modules(harpia.plugins.__path__):
        module = __import__("harpia.plugins." + modname, fromlist="dummy")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and "Type" in obj().get_description():
                block[obj().get_description()["Type"]] = obj

    # Load Examples
    examples = glob(os.environ['HARPIA_DATA_DIR'] + "examples/*")
    for example in examples:
        list_of_examples.append(example)
    list_of_examples.sort()
    
    HarpiaPropertiesControl(properties).load()
    for recent in properties.get_recent_files():
        recent_files.append(recent)



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

