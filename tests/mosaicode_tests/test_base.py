import unittest
from abc import ABCMeta
from mosaicode.GUI.block import Block
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.system import System
from mosaicode.GUI.fieldtypes import *

class TestBase(unittest.TestCase):
    __metaclass__ = ABCMeta

    def create_main_window(self):
        return MainWindow()

    def create_diagram(self):
        return Diagram(self.create_main_window())

    def create_diagram_control(self):
        diagram_control = DiagramControl(self.create_diagram())
        diagram_control.connectors = []
        diagram_control.language = "language"
        return diagram_control

    def create_block(self, diagram_control=None):
        if diagram_control is None:
            diagram_control = self.create_diagram_control()

        block_model = BlockModel()
        block_model.maxIO = 2

        block = Block(diagram_control.diagram, block_model)
        block.language = "language"
        block.properties = [
            {"name": "test",
             "label": "Test",
             "type": "Test"
             }]

        block.ports = [{"type": "Test",
                       "label": "Input",
                       "conn_type": "Input",
                       "name": "input"},
                        {"type": "Test",
                       "label": "Output",
                       "conn_type": "Outpu",
                       "name": "output"}]

        BlockControl.load_ports(block, System.get_ports())

        diagram_control.add_block(block)
        return block

    def create_comment(self):
        comment = Comment(self.create_diagram(), None)
        return comment

    def create_code_template(self):
        code_template = CodeTemplate()
        code_template.name = "webaudio"
        code_template.language = "javascript"
        code_template.command = "python -m webbrowser -t $dir_name$index.html\n"
        code_template.description = "Javascript / webaudio code template"

        code_template.code_parts = ["onload", "function", "declaration", "execution", "html"]
        code_template.properties = [{"name": "title",
                            "label": "Title",
                            "value": "Title",
                            "type": MOSAICODE_STRING
                            }
                           ]

        code_template.files["index.html"] = r"""
<html>
    <head>
        <meta http-equiv="Cache-Control" content="no-store" />
        <!-- $author$ $license$ -->
        <title>$prop[title]$</title>
        <link rel="stylesheet" type="text/css" href="theme.css">
        <script src="functions.js"></script>
        <script>
        $single_code[function]$
        function loadme(){
        $single_code[onload]$
        return;
        }
        var context = new (window.AudioContext || window.webkitAudioContext)();
        //declaration block
        $code[declaration]$

        //execution
        $code[execution]$

        //connections
        $connections$
        </script>
    </head>

    <body onload='loadme();'>
        $code[html]$
    </body>
</html>
"""

        code_template.files["theme.css"] = r"""
/*
Developed by: $author$
*/
html, body {
  background: #ffeead;
  color: #ff6f69;
}
h1, p {
  color: #ff6f69;
}
#navbar a {
  color: #ff6f69;
}
.item {
  background: #ffcc5c;
}
button {
  background: #ff6f69;
  color: #ffcc5c;
}
"""

        code_template.files["functions.js"] = r"""
/*
Developed by: $author$
*/
$single_code[function]$
"""
        return code_template
