# Mosaicode

A Visual Programming Environment and source code generator for specific domains, focusing on Digital Art.

## Getting Started

Getting a copy of the project up and running on your local machine. Supported Platform: GNU/Linux.


### Prerequisites

Open the terminal (Ctrl+Alt+T) and run the following command to install the software dependencies:

```
sudo apt install python3 libgtk-3-dev gir1.2-gtksource-3.0 gir1.2-goocanvas-2.0 python-cairo-dev python3-lxml python3-goocalendar python3-bs4 python3-soupsieve python-gi-dev python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### Installation

Steps to install the Mosaicode in a virtual environment or in the operational system directory.


#### Virtual Environment / Isolated from system directories

Installing python virtual environment via terminal:

```
sudo apt install python3.8-venv
```

Setting the virtual environment:

1. Create the environment: `python3 -m venv <virtual environment name>`
1. Active the environment: `source <virtual environment path>/<virtual environment name>/bin/activate`
1. Install prerequisites: `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev`
1. Install PyGObject: `python -m pip install PyGObject`
1. Install Mosaicode: `python setup.py install`

More details in the Python 3 *Virtual Environments and Packages* documentation: https://docs.python.org/3/tutorial/venv.html

#### Operational System Directories

Run via terminal:

```
sudo python setup.py install
```

## Mosaicode Extensions

Some extensions that you can install to add visual programming languages with resources from areas of computing which allow the development of tools to support Digital Art in a simple and practical way: dragging and connecting blocks:


| Technology  	                | Domain  	         | Extension repository  	                                          | Operating |
| ---	                          | ---	               | ---	                                                            | ---       |
|  Javascript / Web Audio API   | Computer Music  	 | https://github.com/Alice-ArtsLab/mosaicode-javascript-webaudio  	| Yes        |
|  C / OpenCV  	              	| Computer vision  	 | https://github.com/Alice-ArtsLab/mosaicode-c-opencv              | No        |
|  C / Opengl 	    	          | Computer graphics  | https://github.com/Alice-ArtsLab/mosaicode-c-opengl              | No        |
|  Javascript / Canvas 	        | Graphics on a web  | https://github.com/Alice-ArtsLab/mosaicode-javascript-canvas     | No        |
|  C / Linux-Joystick	          | USB Controller  	 | https://github.com/Alice-ArtsLab/mosaicode-c-joystick            | No        |
|  C / Gtk 	                    | GUI                | https://github.com/Alice-ArtsLab/mosaicode-c-gtk                 | No        |
|  C / Portaudio 	              | Computer Music  	 | https://github.com/Alice-ArtsLab/mosaicode-c-sound               | No        |



## Related pages

ALICE. Lab:  [https://alice.dcomp.ufsj.edu.br/](https://alice.dcomp.ufsj.edu.br/)

## Contact

Asking to:

* mosaicode-dev@googlegroups.com
