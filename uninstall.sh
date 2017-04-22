#!/bin/sh
python setup.py install --record files.txt
cat files.txt | xargs rm -rf
rm -rf files.txt
rm -rf /usr/share/harpia
rm -rf build
rm -rf dist
rm -rf ~/harpia/configuration.xml
