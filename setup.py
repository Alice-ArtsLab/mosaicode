# -*- coding: utf-8 -*-

from glob import glob

DISTUTILS_DEBUG = "True"


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
    'Programming Language :: JavaScript',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Code Generators',
]

setup(name='mosaicode',
      install_requires=['beautifulsoup4', 'pip', 'python>=2.7'],
      tests_require=['pytest'],
      test_suite='test',
      version='1.0a7',
      packages=[
          'app_data',
          'mosaicode',
          'mosaicode.utils',
          'mosaicode.persistence',
          'mosaicode.GUI',
          'mosaicode.GUI.components',
          'mosaicode.extensions',
          'mosaicode.control',
          'mosaicode.model'],
      scripts=['launcher/mosaicode', 'scripts/mosaicode.sh','scripts/mosaicode.1'],
      description='Image Processing and Computer Vision \
      Automatic Programming Tool',
      author='Ouroboros',
      author_email='cmagnobarbosa+mosaicode@gmail.com',
      maintainer="Ouroboros",
      maintainer_email="cmagnobarbosa+mosaicode@gmail.com",
      license="GNU GPL3",
      url='http://ges.dcomp.ufsj.edu.br/index.php/ouroboros/',

      # this is fucked up! must put it in package_data!!
      data_files=[
            ('/usr/share/mosaicode/images', glob("app_data/images/*")),
            ('/usr/share/mosaicode/po/pt/LC_MESSAGES/',
                   glob("app_data/po/pt/LC_MESSAGES/*")),
            ('/usr/share/mosaicode/examples', glob("app_data/examples/*.mscd")),
            ('/usr/share/applications/', ["app_data/mosaicode.desktop"]),
            ('/usr/share/icons/hicolor/scalable/apps',
                   ['app_data/images/mosaicode.svg']),
            ('/usr/share/pixmaps', ['app_data/images/mosaicode.svg']),
            ('/usr/share/icons/hicolor/24x24/apps',
                   ['app_data/images/mosaicode.png']), ],
      **config
      )
