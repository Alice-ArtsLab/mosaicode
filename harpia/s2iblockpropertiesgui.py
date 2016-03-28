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

# Libraries
import pygtk
pygtk.require('2.0')
import gtk
from GladeWindow import GladeWindow
import s2idirectory
import os
#----------------------------------------------------------------------

## Implements the Block Properties GUI
class S2iBlockPropertiesGUI:
    """
    This class calls the correct block properties GUI for each block.
    Implements some functionalitites that verify which block is beeing edited and call the correct GUI for the current block.
    Allows the user to chance the block appearance and Toggle the block state.
    """

    #----------------------------------------------------------------------

    def __init__( self, a_oS2iBlock ):
        """
        Constructor. Receives a s2iBlock and sets the member atributte s2iBlock with this argument.
        """
        ## S2i Block member atributte.
        self.m_oS2iBlock = a_oS2iBlock
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
    
    #----------------------------------------------------------------------

    def __del__(self):
        pass

    #----------------------------------------------------------------------

#--------S2IPROPERTIESGUI PUBLIC FUNCTIONS--------------
    
    #----------------------------------------------------------------------

    def EditProperties( self, a_oPropertiesXML ): 
        """
        This function calls the correct .glade file, based on the block type. The block type is found using the PropertiesXML argument.
        """
        
        #Load block type from a_oPropertiesXML
        #BlockType = int(a_oPropertiesXML.properties.block.type)
        BlockType = int(a_oPropertiesXML.getChildTagAttr("properties", "block", "type"))
        PkgName = 'harpia.bpGUI.'
        ModName = str(s2idirectory.block[BlockType]["Path"]["Python"])
        #from spam.ham import eggs" results in "
        harpia_bpGUI_Mod = __import__(PkgName, globals(), locals(), [ModName])
        guiMod = getattr(harpia_bpGUI_Mod, ModName)
        
        PropertiesGUI = guiMod.Properties(a_oPropertiesXML, self)
        PropertiesGUI.show( center=0 )
        
        # Executes the file based on the block name
        
    #----------------------------------------------------------------------

    def SetPropertiesXML( self, a_oPropertiesXML ): 
        """
        Sets the PropertiesXML with the propertiesXML argument.
        """
        self.m_oS2iBlock.SetPropertiesXML(a_oPropertiesXML)
        
    #----------------------------------------------------------------------

    def GetState(self):
        """
        Returns the block state.
        """
        return  self.m_oS2iBlock.get_state()

    #----------------------------------------------------------------------

    def GetBorderColor( self,*args ):
        """
        Returns the block border color.
        """

        return self.m_oS2iBlock.GetBorderColor()

    #----------------------------------------------------------------------

    def GetBackColor(self,*args):
        """
        Returns the block back color.
        """
        return self.m_oS2iBlock.GetBackColor()
    
    #----------------------------------------------------------------------

    def SetBorderColor( self, a_oBorderColor ):
        """
        Sets the border color.
        """
        self.m_oS2iBlock.SetBorderColor(a_oBorderColor)

    #----------------------------------------------------------------------

    def SetBackColor(self,a_oBackColor):
        """
        Sets the block BackColor.
        """
        self.m_oS2iBlock.SetBackColor(a_oBackColor)

    #----------------------------------------------------------------------
