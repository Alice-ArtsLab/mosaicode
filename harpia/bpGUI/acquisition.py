#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Acquisition(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "00"

    # ----------------------------------------------------------------------
    def get_help(self):

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Image"),
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":"",
                 "OutTypes":{0:"HRP_IMAGE"},
                 "Description":_("Create a new image or load image from a source, such as file, camera, frame grabber."),
                 "TreeGroup":_("General"),
                 "IsSource":True
         }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
#----------------------------------------------------------------------

class Properties( GladeWindow, S2iCommonProperties):

    #----------------------------------------------------------------------

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):

        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']

        filename = self.m_sDataDir+'glade/acquisition.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'ACQURadioFile',
            'ACQURadioNewImage',
            'ACQURadioCapture',
            'ACQURadioLive',
            'ACQURadioVideo',
            'ACQULabelFileProperty',
            'ACQULabelFilename',
            'ACQUFilename',
            'video_name',
            'video_name_BT',
            'video_name_LABEL',
            'video_name_LABEL2',
            'ACQUButtonSearch',
            'ACQULabelNewImage',
            'ACQULabelImageSize',
            'ACQULabelWidth',
            'ACQULabelHeight',
            'ACQUWidth',
            'ACQUHeight',
            'ACQULabelCameraProperty',
            'ACQULabelCamera',
            'ACQUCamera',
            'ACQULabelSize',
            'ACQUSize',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'frameRate_Label',
            'frameRate',
            'streamProperties_label',
            'frameRate_label2',
                        'acquisition_confirm'
            ]

        handlers = [
            'on_ACQURadioFile_pressed',
            'on_ACQURadioNewImage_pressed',
            'on_ACQURadioCapture_pressed',
            'on_ACQURadioLive_pressed',
            'on_ACQUButtonSearch_clicked',
            'on_ACQUVideoSearch_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_ACQURadioVideo_pressed',
            'on_acquisition_confirm_clicked',
            'on_cancel_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.m_nNumAvailableCams = 4

        if os.name == 'posix':
          self.m_nNumAvailableCams = 0
          t_lListVidDevs = glob("/dev/video*")
          self.m_nNumAvailableCams = len(t_lListVidDevs)

        self.widgets['ACQUCamera'].remove_text(0)
        for cam in range(self.m_nNumAvailableCams):
          self.widgets['ACQUCamera'].append_text(str("/dev/video"+ str(cam)))
        self.widgets['ACQUCamera'].append_text(str("Default"))



        self.m_sCurrentActive = 'file'
        #load properties values
        block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        for Property in block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "type":
                if value == "file":
                    self.widgets['ACQURadioFile'].set_active( True );
                    self.on_ACQURadioFile_pressed()
                elif value == "camera":
                    self.widgets['ACQURadioCapture'].set_active( True );
                    self.on_ACQURadioCapture_pressed()
                    self.m_sCurrentActive = 'camera'
                elif value == "live":
                    self.widgets['ACQURadioLive'].set_active( True );
                    self.on_ACQURadioLive_pressed()
                    self.m_sCurrentActive = 'live'
                elif value == "video":
                    self.widgets['ACQURadioVideo'].set_active( True );
                    self.on_ACQURadioVideo_pressed()
                    self.m_sCurrentActive = 'video'
                else:
                    self.widgets['ACQURadioNewImage'].set_active( True );
                    self.on_ACQURadioNewImage_pressed()
                    self.m_sCurrentActive = 'newimage'
            if name == "filename":
                self.widgets['ACQUFilename'].set_text( value );
            if name == "video_name":
                self.widgets['video_name'].set_text( value );

            if name == "camera" or name == 'live':
              if os.name == 'posix':
                if int(value) < self.m_nNumAvailableCams:
                  self.widgets['ACQUCamera'].set_active( int(value) );
                else:
                  self.widgets['ACQUCamera'].set_active(self.m_nNumAvailableCams); #will set None

            if name == "frameRate":
                self.widgets['frameRate'].set_value(float(value));

            # Use the property size to set the New Image size too.
            if name == "size":
                if value == "1024x768":
                    self.widgets['ACQUSize'].set_active( 0 );
                if value == "800x600":
                    self.widgets['ACQUSize'].set_active( 1 );
                if value == "832x624":
                    self.widgets['ACQUSize'].set_active( 2 );
                if value == "640x480":
                    self.widgets['ACQUSize'].set_active( 3 );
                else:
                    self.widgets['ACQUSize'].set_active( 0 );
                # New Image size

                self.widgets['ACQUWidth'].set_value( float(value[ :value.find('x')]) )
                self.widgets['ACQUHeight'].set_value( float( value[value.find('x')+1: ]) )



        self.configure()

        #load help text
        #t_oS2iHelp = bt.bind_file("../etc/acquisition/acquisition.help")
        # t_oS2iHelp = XMLParser(self.m_sDataDir+"help/acquisition"+ _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.getTag("help").getTag("content").getTagContent()) ) )

        # self.widgets['HelpView'].set_buffer( t_oTextBuffer )

    #----------------------------------------------------------------------

    def __del__(self):
        pass

    #----------------------------------------------------------------------

    def on_acquisition_confirm_clicked( self, *args ):
        self.widgets['acquisition_confirm'].grab_focus()
        t_sFilename = unicode(self.widgets['ACQUFilename'].get_text())

        block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        for Property in block_properties:
            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "state":
                if self.m_oS2iBlockProperties.GetState():
                    Property.setAttr("value", "true")
                else:
                    Property.setAttr("value", "false")

            #file selected
            new_value = value
            if name == "type":
                if self.widgets['ACQURadioFile'].get_active():
                    new_value = u"file"
                    self.m_sCurrentActive = 'file'
                elif self.widgets['ACQURadioCapture'].get_active():
                    new_value = u"camera"
                    self.m_sCurrentActive = 'camera'
                elif self.widgets['ACQURadioLive'].get_active():
                    new_value = u"live"
                    self.m_sCurrentActive = 'live'
                elif self.widgets['ACQURadioVideo'].get_active():
                    new_value = u"video"
                    self.m_sCurrentActive = 'video'
                else:
                    new_value = u"newimage"
                    self.m_sCurrentActive = 'newimage'


            if name == "filename":
                new_value = unicode(t_sFilename)
            if name == "video_name":
                new_value = unicode(unicode(self.widgets['video_name'].get_text()))
            #capture selected
            if name == "frameRate":
                new_value = unicode(str(self.widgets['frameRate'].get_value()))

            if name == "camera" or name == 'live':
              Camera = self.widgets['ACQUCamera'].get_active_text()
              if Camera <> u'Default':
                try:
                  if os.name == 'posix':
                    new_value = unicode(Camera.split('video')[1]) ## getting rid of the /dev/video
                  else:
                    new_value = unicode(Camera) ## just the num
                except:
                  new_value = unicode("-1")
              else:
                new_value = unicode('-1')

            if name == "size":
                if self.m_sCurrentActive == 'camera' or self.m_sCurrentActive == 'live':
                    Size = int(self.widgets['ACQUSize'].get_active())
                    if Size == 0:
                        new_value = unicode("1024x768")
                    if Size == 1:
                        new_value = unicode("800x600")
                    if Size == 2:
                        new_value = unicode("832x624")
                    if Size == 3:
                        new_value = unicode("640x480")

                if self.m_sCurrentActive == 'newimage':
                    Width = int(self.widgets['ACQUWidth'].get_value())
                    Height = int(self.widgets['ACQUHeight'].get_value())
                    new_value = unicode( str(Width) + 'x' + str(Height) )

            Property.setAttr("value", new_value)

        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()

    #------------------------Help Text----------------------------------------------

    def getHelp(self):#adicionado help
        return "Realiza a aquisição de uma imagem a partir de algum dispositivo,\
        seja este uma mídia ou um dispositivo de aquisição de imagens (câmera, scanner)."

    def on_ACQUButtonSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Abrir...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

#-------------
#Scotti
        if os.name == 'posix':
          dialog.set_current_folder("/home/" + str(os.getenv('USER')) + "/Desktop")
#Scotti

        dialog.add_filter(AllFileFilter())
        dialog.add_filter(JPGFileFilter())

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['ACQUFilename'].set_text(response);

    #----------------------------------------------------------------------

    def on_ACQUVideoSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Abrir...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

#-------------
#Scotti
        if os.name == 'posix':
          dialog.set_current_folder("/home/" + str(os.getenv('USER')) + "/Desktop")
#Scotti

        dialog.add_filter(AllFileFilter())
        dialog.add_filter(AVIFileFilter())
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['video_name'].set_text(response);

    #----------------------------------------------------------------------


    def on_ACQURadioFile_pressed( self, *args ):

        self.widgets['ACQULabelCameraProperty'].set_sensitive( False )
        self.widgets['ACQULabelCamera'].set_sensitive( False )
        self.widgets['ACQUCamera'].set_sensitive( False )
        self.widgets['ACQULabelSize'].set_sensitive( False )
        self.widgets['ACQUSize'].set_sensitive( False )

        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )

        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )

        self.widgets['ACQULabelFileProperty'].set_sensitive( True )
        self.widgets['ACQULabelFilename'].set_sensitive( True )
        self.widgets['ACQUFilename'].set_sensitive( True )
        self.widgets['ACQUButtonSearch'].set_sensitive( True )

        self.widgets['frameRate_Label'].set_sensitive( False )
        self.widgets['frameRate'].set_sensitive( False )
        self.widgets['streamProperties_label'].set_sensitive( False )
        self.widgets['frameRate_label2'].set_sensitive( False )

    #----------------------------------------------------------------------

    def on_ACQURadioCapture_pressed( self, *args ):

        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )

        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )

        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )

        self.widgets['ACQULabelCameraProperty'].set_sensitive( True )
        self.widgets['ACQULabelCamera'].set_sensitive( True )
        self.widgets['ACQUCamera'].set_sensitive( True )
        self.widgets['ACQULabelSize'].set_sensitive( True )
        self.widgets['ACQUSize'].set_sensitive( True )

        self.widgets['frameRate_Label'].set_sensitive( False )
        self.widgets['frameRate'].set_sensitive( False )
        self.widgets['streamProperties_label'].set_sensitive( False )
        self.widgets['frameRate_label2'].set_sensitive( False )

    #----------------------------------------------------------------------
    def on_ACQURadioNewImage_pressed( self, *args ):

        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )

        self.widgets['ACQULabelCameraProperty'].set_sensitive( False )
        self.widgets['ACQULabelCamera'].set_sensitive( False )
        self.widgets['ACQUCamera'].set_sensitive( False )
        self.widgets['ACQULabelSize'].set_sensitive( False )
        self.widgets['ACQUSize'].set_sensitive( False )

        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )

        self.widgets['ACQULabelNewImage'].set_sensitive( True )
        self.widgets['ACQULabelImageSize'].set_sensitive( True )
        self.widgets['ACQULabelWidth'].set_sensitive( True )
        self.widgets['ACQULabelHeight'].set_sensitive( True )
        self.widgets['ACQUWidth'].set_sensitive( True )
        self.widgets['ACQUHeight'].set_sensitive( True )

        self.widgets['frameRate_Label'].set_sensitive( False )
        self.widgets['frameRate'].set_sensitive( False )
        self.widgets['streamProperties_label'].set_sensitive( False )
        self.widgets['frameRate_label2'].set_sensitive( False )

    def on_ACQURadioLive_pressed( self, *args ):
        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )

        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )

        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )

        self.widgets['ACQULabelCameraProperty'].set_sensitive( True )
        self.widgets['ACQULabelCamera'].set_sensitive( True )
        self.widgets['ACQUCamera'].set_sensitive( True )
        self.widgets['ACQULabelSize'].set_sensitive( True )
        self.widgets['ACQUSize'].set_sensitive( True )

        self.widgets['frameRate_Label'].set_sensitive( True )
        self.widgets['frameRate'].set_sensitive( True )
        self.widgets['streamProperties_label'].set_sensitive( True )
        self.widgets['frameRate_label2'].set_sensitive( True )

    def on_ACQURadioVideo_pressed( self, *args ):
        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )

        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )

        self.widgets['video_name'].set_sensitive( True )
        self.widgets['video_name_BT'].set_sensitive( True )
        self.widgets['video_name_LABEL'].set_sensitive( True )
        self.widgets['video_name_LABEL2'].set_sensitive( True )

        self.widgets['ACQULabelCameraProperty'].set_sensitive( False )
        self.widgets['ACQULabelCamera'].set_sensitive( False )
        self.widgets['ACQUCamera'].set_sensitive( False )
        self.widgets['ACQULabelSize'].set_sensitive( False )
        self.widgets['ACQUSize'].set_sensitive( False )

        self.widgets['frameRate_Label'].set_sensitive( True )
        self.widgets['frameRate'].set_sensitive( True )
        self.widgets['streamProperties_label'].set_sensitive( True )
        self.widgets['frameRate_label2'].set_sensitive( True )

    #----------------------------------------------------------------------

#AcquisitionProperties = Properties( )
#AcquisitionProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
   import harpia.gerador
   for propIter in blockTemplate.properties:
       if propIter[0] == 'type':
           flag = propIter[1]

       if ((propIter[0] == 'filename') and (flag == 'file')):
           argFilename = propIter[1]

       if ((propIter[0] == 'size') and (flag == 'newimage')):
           size = propIter[1]
           Width = size[ :size.find('x')]
           Height = size[size.find('x')+1: ]

       if (propIter[0] == 'camera' and flag == 'live'):
           tmpPack = [] #contendo [ blockNumber , camNum ]
           tmpPack.append(blockTemplate.blockNumber)
           harpia.gerador.g_bLive.append(tmpPack)
           blockTemplate.imagesIO += 'CvCapture * block$$_capture = NULL;\n' + \
                    'IplImage * block$$_frame = NULL;\n' + \
                    'block$$_capture = cvCaptureFromCAM(' + propIter[1] + ');\n'

       if (propIter[0] == 'camera' and flag == 'camera'):
           captureCamNumber = propIter[1]

       if(propIter[0] == 'video_name' and flag == 'video'):
           tmpPack = []
           tmpPack.append(blockTemplate.blockNumber)
           harpia.gerador.g_bLive.append(tmpPack)
           blockTemplate.imagesIO += 'CvCapture * block$$_capture = NULL;\n'+ \
                    'IplImage * block$$_frame = NULL;\n' + \
                    'block$$_capture = cvCreateFileCapture("' + propIter[1] + '");\n'
       if propIter[0] == 'frameRate':
           if float(propIter[1]) > harpia.gerador.g_bFrameRate:
            harpia.gerador.g_bFrameRate = float(propIter[1])
   blockTemplate.imagesIO += 'IplImage * block$$_img_o1 = NULL; //Capture\n'

   if flag == 'camera':
       blockTemplate.functionCall = \
           'CvCapture* block$$_capture = NULL; \n' + \
           'IplImage* block$$_frame = NULL; \n' + \
           'block$$_capture = cvCaptureFromCAM(' + captureCamNumber + '); \n' + \
           'if( !cvGrabFrame( block$$_capture ) \n ) { printf("Cannot Grab Image from camera '+ captureCamNumber +'"); }' + \
           'block$$_frame = cvRetrieveFrame( block$$_capture ); ' + \
           'if( !cvGrabFrame( block$$_capture ) \n ) { printf("Cannot Grab Image from camera '+ captureCamNumber +'"); }' + \
           'block$$_frame = cvRetrieveFrame( block$$_capture ); ' + \
           'if( !cvGrabFrame( block$$_capture ) \n ) { printf("Cannot Grab Image from camera '+ captureCamNumber +'"); }' + \
           'block$$_frame = cvRetrieveFrame( block$$_capture ); ' + \
           'block$$_img_o1 = cvCloneImage( block$$_frame );\n'

   if flag == 'video':
       blockTemplate.functionCall = '// Video Mode \n' + \
           'block$$_img_o1 = cvCloneImage(block$$_frame);\n'
       blockTemplate.outDealloc += 'cvReleaseCapture(&block$$_capture);\n'

   if flag == 'file':
       blockTemplate.imagesIO += \
        'char block$$_arg_Filename[] = "' + argFilename + '";\n'
       blockTemplate.functionCall = \
           'block$$_img_o1 = cvLoadImage(block$$_arg_Filename,-1);\n'

   if flag == 'live':
       blockTemplate.functionCall = '// Live Mode \n' + \
           'block$$_img_o1 = cvCloneImage( block$$_frame );\n'
       blockTemplate.outDealloc += 'cvReleaseCapture(&block$$_capture);\n'

   if flag == 'newimage':
       blockTemplate.functionCall = \
            'CvSize size = cvSize(' + Width +','+ Height +');\n' + \
            'block$$_img_o1 = cvCreateImage(size,IPL_DEPTH_8U,3);\n' + \
            'cvSetZero(block$$_img_o1);\n'
   blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n'

# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label":_("Image"),
         "Path":{"Python":"acquisition",
                 "Glade":"glade/acquisition.ui",
                 "Xml":"xml/acquisition.xml"},
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":"",
                 "OutTypes":{0:"HRP_IMAGE"},
                 "Description":_("Create a new image or load image from a source, such as file, camera, frame grabber."),
                 "TreeGroup":_("General"),
                 "IsSource":True
         }
