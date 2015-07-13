# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
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


#i18n
import gettext
APP='harpia'
DIR='/usr/share/harpia/po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

TIPS_VER = "v0.86"

TIPS = (

		_("Use the toolbox located on the left side of the screen\n"
			"to select a block. Drag 'n Drop it on the white\n"
			"canvas to start a processing chain, click on the\n"
			"`Run` button (or press F9) to execute it."),

		_("Blocks may have inputs and/or outputs. Clicking\n"
			"on one output (at the right side of the \n"
			"block) will initiate a connector; clicking on an \n"
			"input (left side) will confirm it."),

		_("To view each block's properties (e.g. parameters,\n"
			"thresholds, filenames), click twice on the block.\n"
			"For the `Show Image` block, clicking twice on it \n"
			"will show the processed image."),

		_("When viewing a live feed (video from files or \n"
			"streams), press any key to exit (while selecting\n"
			"the video output window)."),

		_("Useful commented examples can be accessed within\n"
			"the help menu. Each example has a Comment block;\n"
			"click twice on it to see the comments"),

		_("Blocks and Connectors may or not have `information\n"
			"flow`. Blocks with flow are indicated by black border\n"
			"and more opaque background; red border means no\n"
			"flow. Bold connectors have flow, thin ones don't.\n"
			"Blocks without `information flow` won't be processed."),
			
		_("`Information flow` is propagated through blocks\n"
			"starting from the `source` blocks (blocks without\n"
			"inputs). A block with all its inputs connected to\n"
			"`flowing` connectors will have flow."),

		_("In the top of the block selection toolbox, there\n"
			"is a search field (Ctrl+F). Enter the name of the \n"
			"operation to quickly find it"),

		_("Outputs and inputs are of a given type (e.g. image,\n"
			"point, rectangle, double number). Connections are only\n"
			"possible between ports of the same type."),

		_("The 'Run Command' block can execute system calls\n"
			"using the input value as a parameter or as a trigger."),

		)
