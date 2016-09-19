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
from harpia.control.preferencescontrol import *
from harpia.model.preferences import *

import pkgutil # For dynamic package load
import inspect # For module inspect

from glob import glob # To load examples
import os
import copy

import sys

import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

Log = None

properties = Preferences()

block = {}
list_of_examples = []
recent_files = []

def load_blocks():
    for importer, modname, ispkg in pkgutil.walk_packages(
                    harpia.plugins.__path__,
                    harpia.plugins.__name__ + ".",
                    None):
        if ispkg:
            continue
        module = __import__(modname, fromlist="dummy")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and "Type" in obj().get_description():
                block[obj().get_description()["Type"]] = obj

def load():
    load_blocks()

    examples = glob(os.environ['HARPIA_DATA_DIR'] + "examples/*")
    for example in examples:
        list_of_examples.append(example)
    list_of_examples.sort()
    
    PreferencesControl(properties).load()
    for recent in properties.get_recent_files():
        recent_files.append(recent)



#HERE: ADD TYPED ICONS for inputs and outputs
icons = {
    "IconInput":"images/s2iinput.png",
    "IconOutput":"images/s2ioutput.png"
    }

connections = {
        "HRP_INT":{
            "icon_in":"images/s2iintin.png",
            "icon_out":"images/s2iintout.png",
            "code": 'block$to_block$_int_i$to_block_in$ = block$from_block$_int_o$from_block_out$;// INT conection\n'
            },
        "HRP_DOUBLE":{
            "icon_in":"images/s2idoubin.png",
            "icon_out":"images/s2idoubout.png",
            "code": 'block$to_block$_double_i$to_block_in$ = block$from_block$_double_o$from_block_out$;// DOUBLE conection\n'
            },
        "HRP_RECT":{
            "icon_in":"images/s2irctin.png",
            "icon_out":"images/s2irctout.png",
            "code": 'block$to_block$_rect_i$to_block_in$ = block$from_block$_rect_o$from_block_out$;// RECT conection\n'
            },
        "HRP_IMAGE":{
            "icon_in":"images/s2iinput.png",
            "icon_out":"images/s2ioutput.png",
            "code": 'block$to_block$_img_i$to_block_in$ = cvCloneImage(block$from_block$_img_o$from_block_out$);// IMG conection\n'
            },
        "HRP_POINT":{
            "icon_in":"images/s2ipointin.png",
            "icon_out":"images/s2ipointout.png",
            "code": 'block$to_block$_point_i$to_block_in$ = block$from_block$_point_o$from_block_out$;// POINT conection\n'
            },
        "HRP_WEBAUDIO_SOUND":{
            "icon_in":"images/s2irctin.png",
            "icon_out":"images/s2irctout.png",
            "code": 'block$to_block$_rect_i$to_block_in$ = block$from_block$_rect_o$from_block_out$;// RECT conection\n'
            }
        }

