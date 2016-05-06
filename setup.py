# -*- coding: utf-8 -*-
DISTUTILS_DEBUG="True"

from glob import glob
#from distutils.core import setup
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {}

config['classifiers'] = [
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'Intended Audience :: Science/Research',
			'License :: OSI Approved :: GNU General Public License (GPL)',
			'Natural Language :: English',
			'Operating System :: OS Independent',
			'Programming Language :: C',
			'Programming Language :: Python',
			'Topic :: Scientific/Engineering',
			'Topic :: Software Development :: Code Generators',
			]

setup(name='harpia',
            install_requires=['beautifulsoup4'],
			version='1.0',
			packages=['harpia','harpia.bpGUI', 'harpia.utils', 'harpia.GUI', 'harpia.control'],
			scripts=['launcher/harpia'],
			description='Image Processing and Computer Vision Automatic Programming Tool',
			author='Clovis Peruchi Scotti',
			author_email='scotti@ieee.org',
			maintainer="Clovis Peruchi Scotti",
			maintainer_email="scotti@ieee.org",
			license="GNU GPL",
			url='http://s2i.das.ufsc.br/harpia/en/home.html',
			data_files=[ ('/usr/share/harpia/images', glob("app_data/images/*")), #this is fucked up! must put it in package_data!!
		 							 ('/usr/share/harpia/xml', glob("app_data/xml/*.xml")), #same thing
		 							 ('/usr/share/harpia/po/pt/LC_MESSAGES/', glob("app_data/po/pt/LC_MESSAGES/*")),
		 							 ('/usr/share/harpia/glade', glob("app_data/glade/*.ui")),
		 							 ('/usr/share/harpia/examples', glob("app_data/examples/*.hrp")),
		 							 ('/usr/share/applications/', ["app_data/harpia.desktop"]),
									 ('/usr/share/icons/hicolor/scalable/apps', ['app_data/images/harpia.svg']),
									 ('/usr/share/pixmaps', ['app_data/images/harpia.svg']),
									 ('/usr/share/icons/hicolor/24x24/apps', ['app_data/images/harpia.png']),],
			**config
			)
