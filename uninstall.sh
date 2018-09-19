#!/bin/sh
python setup.py install --record files.txt
cat files.txt | xargs rm -rf
rm -rf files.txt
rm -rf /usr/share/mosaicode
rm -rf build
rm -rf dist
rm -rf mosaicode.egg-info
rm -rf ~/mosaicode/configuration.xml
rm -rf /usr/local/lib/python2.7/dist-packages/mosaicode-1.0.4.dev1-py2.7.egg
