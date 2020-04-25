# -*- coding: utf-8 -*-

from glob import glob

DISTUTILS_DEBUG = "True"


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    author='ALICE: Arts Lab in Interfaces, Computers, and Else',
    author_email='mosaicode-dev@googlegroups.com',
    description='Automatic Programming Tool',
    install_requires=[
            "PyGObject",
            "GooCalendar",
            "BeautifulSoup4",
            "lxml",
            "pgi"],
    license="GNU GPL3",
    maintainer="ALICE: Arts Lab in Interfaces, Computers, and Else",
    maintainer_email="mosaicode-dev@googlegroups.com",
    name='mosaicode',
    packages=find_packages(exclude=["tests.*", "tests"]),
    python_requires='>=2.7',
    scripts=['launcher/mosaicode', 'scripts/mosaicode.sh','scripts/mosaicode.1'],
    test_suite='tests',
    tests_require=['pytest'],
    url='https://alice.dcomp.ufsj.edu.br/mosaicode/',
    version='1.0.4.dev1',

    # this is fucked up! must put it in package_data!!
    data_files=[
            ('/usr/share/applications/',
            ["app_data/mosaicode.desktop"]),
            ('/usr/share/icons/hicolor/scalable/apps',
            ['app_data/mosaicode.png']),
            ('/usr/share/pixmaps',
            ['app_data/mosaicode.png']),
            ('/usr/share/icons/hicolor/24x24/apps',
            ['app_data/mosaicode.png'])],
    classifiers=[
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
    ],
    )
