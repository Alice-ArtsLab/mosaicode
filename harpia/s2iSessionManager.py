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

import time
from harpia.utils.XMLUtils import XMLParser

from gerador import *
from constants import *

class s2iSessionManager:
    session_id = 0
    dir_name = "harpiaBETMP0"
    old_path = ""

#----------------------------------------------------------------------
    def __init__(self):
        self.session_id = str(time.time())
        self.dir_name += self.session_id
        self.old_path = os.path.realpath(os.curdir)

#----------------------------------------------------------------------
    def __make_dir(self):
        os.chdir(TMPDIR)
        os.mkdir(self.dir_name)
        return

#----------------------------------------------------------------------
    def __store_XML(self, a_lsXML=["<harpia></harpia>"]):
        # try:
        os.chdir(TMPDIR + '/' + self.dir_name)
        t_oStoreFile = file('imageProcessingChain.xml', 'w')
        t_oStoreFile.write(a_lsXML[0])
        t_oStoreFile.close()
        # except:
        # print "Problems Saving xml"
        return

#----------------------------------------------------------------------
    def __run_generator(self):
        # changes dir...
        os.chdir(TMPDIR + '/' + self.dir_name)

        for step in parseAndGenerate(self.dir_name, 'imageProcessingChain.xml', "/"):
            yield step

        # comes back to original dir
        os.chdir(self.old_path)
        return

#----------------------------------------------------------------------
    def new_instance(self, a_lsXML=["<harpia></harpia>"]):
        self.__make_dir()
        self.__store_XML(a_lsXML)
        for step in self.__run_generator():
            yield step
        return
