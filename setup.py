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
      install_requires=["PyGObject", "GooCalendar", "BeautifulSoup4", "lxml", "pgi", "mosaicomponents"],
      python_requires='>=2.7',
      tests_require=['pytest'],
      test_suite='tests',
      version='1.0.4.dev1',
      packages=find_packages(exclude=["tests.*", "tests"]),
      scripts=['launcher/mosaicode', 'scripts/mosaicode.sh','scripts/mosaicode.1'],
      description='Image Processing and Computer Vision \
      Automatic Programming Tool',
      author='ALICE: Arts Lab in Interfaces, Computers, and Experiences',
      author_email='mosaicode-dev@googlegroups.com',
      maintainer="ALICE: Arts Lab in Interfaces, Computers, and Experiences",
      maintainer_email="mosaicode-dev@googlegroups.com",
      license="GNU GPL3",
      url='http://mosaicode.github.io/',

      # this is fucked up! must put it in package_data!!
      data_files=[
            ('/usr/share/mosaicode/images', glob("app_data/images/*")),
            ('/usr/share/mosaicode/po/pt/LC_MESSAGES/', glob("app_data/po/pt/LC_MESSAGES/*")),
            ('/usr/share/applications/', ["app_data/mosaicode.desktop"]),
            ('/usr/share/icons/hicolor/scalable/apps', ['app_data/images/mosaicode.png']),
            ('/usr/share/pixmaps', ['app_data/images/mosaicode.png']),
            ('/usr/share/icons/hicolor/24x24/apps', ['app_data/images/mosaicode.png'])],
      zip_safe=False,
      **config
      )
