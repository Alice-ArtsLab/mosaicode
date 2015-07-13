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

import time
import sys
import os

from amara import binderytools as bt

from gerador import *

class s2iSessionManager:
	m_sSessionId = 0
	m_sDirName = "harpiaBETMP0"
	TMPDIR = "/tmp/"
	
	HARPIARESPONSE="""
<harpiamessage>
    <session value="88"/>
	<version value="88"/>
	<commands>
		<command name="newsession">
			<param name="status">completed</param>
			<param name="session">666</param>
			<param name="block"></param>
			<param name="output"></param>
			<param name="data"></param>
		</command>
	</commands>
</harpiamessage>
"""
	
	m_sOldPath = ""
	
	def __init__(self ):
		self.m_sSessionId = str(time.time())
		self.m_sDirName += self.m_sSessionId
		self.m_sOldPath = os.path.realpath(os.curdir)
	
	
	def MakeDir(self ):
		os.chdir(self.TMPDIR)
		os.mkdir(self.m_sDirName)
		return
	
	def StoreXML(self , a_lsXML = ["<harpia></harpia>"]):
		#try:
		os.chdir(self.TMPDIR + '/' + self.m_sDirName)
		t_oStoreFile = file('imageProcessingChain.xml', 'w')
		t_oStoreFile.write(a_lsXML[0])
		t_oStoreFile.close()
		#except:
			#print "Problems Saving xml"
		return
	
	def RunGerador(self ):
		#changes dir...
		os.chdir(self.TMPDIR + '/' + self.m_sDirName)
		#This is totally useless... it works with nothing
		INSTALLDIR = "/"
		#This is totally useless... it works with nothing
		
		for step in parseAndGenerate(self.m_sDirName,'imageProcessingChain.xml',INSTALLDIR):
			yield step
		
		#comes back to original dir
		os.chdir(self.m_sOldPath)
		
		return
	
	def ReturnResponse(self ):
		t_oResponse = bt.bind_string(self.HARPIARESPONSE)
		return t_sResponse
	
	def NewInstance(self , a_lsXML = ["<harpia></harpia>"]):
		self.MakeDir()
		self.StoreXML(a_lsXML)
		for step in self.RunGerador():
			yield step
		return
	
	