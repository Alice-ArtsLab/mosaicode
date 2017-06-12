#!/bin/sh
python setup.py install --record files.txt
cat files.txt | xargs rm -rf
rm -rf files.txt
rm -rf /usr/share/mosaicode
rm -rf build
rm -rf dist
rm -rf ~/mosaicode/configuration.xml
