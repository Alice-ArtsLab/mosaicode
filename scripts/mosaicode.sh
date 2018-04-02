echo "Solving dependencies problems"
sudo apt-get --yes install libopencv-dev python-opencv
sudo apt-get --yes install python-gtk2 python-glade2
sudo apt-get --yes install python-gnome2
sudo apt-get --yes install libgoocanvas-2.0-common
sudo apt-get --yes install gir1.2-goocanvas-2.0
sudo apt-get --yes install python-lxml
sudo apt --yes install python-gi
sudo cp /usr/local/bin/mosaicode.1 /usr/share/man/man1
sudo gzip /usr/share/man/man1/mosaicode.1
