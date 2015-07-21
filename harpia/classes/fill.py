import gettext
_ = gettext.gettext

class Fill():

	def generate(self, blockTemplate):
		for propIter in blockTemplate.properties:
			if propIter[0] == 'red':
  				red = propIter[1]
			elif propIter[0] == 'green':
				green = propIter[1]
			elif propIter[0] == 'blue':
				blue = propIter[1]
		blockTemplate.imagesIO = \
			'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
			'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
		blockTemplate.functionCall = \
			'\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
			'block' + blockTemplate.blockNumber + '_img_o1 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_i1);\n' + \
			'\nCvScalar color = cvScalar('+blue +','+ green +','+ red+',0);\n' + \
			'\ncvSet(block' + blockTemplate.blockNumber + '_img_o1,color,NULL);}\n'
		blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
         'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'

	def getBlock(self):
		return {"Label":_("Fill image"),
         "Path":{"Python":"fill",
                 "Glade":"glade/fill.ui",
                 "Xml":"xml/fill.xml"},
         "Inputs":1,
         "Outputs":1,
         "Icon":"images/fill.png",
         "Color":"50:100:200:150",
				 "InTypes":{0:"HRP_IMAGE"},
				 "OutTypes":{0:"HRP_IMAGE"},
				 "Description":_("Fill an image with the desired color."),
				 "TreeGroup":_("General")
         }
