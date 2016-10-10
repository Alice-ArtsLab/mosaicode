# -*- coding: utf-8 -*-
DISTUTILS_DEBUG = "True"

from glob import glob

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {}

config['classifiers'] = [
    'Development Status :: 3 - Alpha',
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
      install_requires=['beautifulsoup4', 'pip'],
      tests_require=['pytest'],
      test_suite='test',
      version='1.0a3',
      packages=[
          'app_data',
          'harpia',
          'harpia.utils',
          'harpia.GUI',
          'harpia.GUI.components',
          'harpia.plugins',
          'harpia.plugins.C',
          'harpia.plugins.C.openCV',
          'harpia.plugins.javascript',
          'harpia.plugins.javascript.webaudio',
          'harpia.control',
          'harpia.model'],
      scripts=['launcher/harpia', 'scripts/harpia.sh'],
      description='Image Processing and Computer Vision Automatic Programming Tool',
      author='Ouroboros',
      author_email='cmagnobarbosa+harpia@gmail.com',
      maintainer="Ourobos",
      maintainer_email="cmagnobarbosa+harpia@gmail.com",
      license="GNU GPL",
      url='http://ges.dcomp.ufsj.edu.br/index.php/ouroboros/',

      data_files=[('/usr/share/harpia/images', glob("app_data/images/*")),  # this is fucked up! must put it in package_data!!
                  ('/usr/share/harpia/po/pt/LC_MESSAGES/',
                   glob("app_data/po/pt/LC_MESSAGES/*")),
                  ('/usr/share/harpia/examples',
                   glob("app_data/examples/*.hrp")),
                  ('/usr/share/applications/',
                   ["app_data/harpia.desktop"]),
                  ('/usr/share/icons/hicolor/scalable/apps',
                   ['app_data/images/harpia.svg']),
                  ('/usr/share/pixmaps',
                   ['app_data/images/harpia.svg']),
                  ('/usr/share/icons/hicolor/24x24/apps', ['app_data/images/harpia.png']), ],
      **config
      )
