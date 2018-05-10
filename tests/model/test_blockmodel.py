from tests.test_base import TestBase
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.fieldtypes import *

class TestBlockModel(TestBase):

    def setUp(self):
        self.block = self.create_block()
        str(self.block)

    def test_color(self):
        self.block.color = "#000000000000"
        self.assertEqual(self.block.get_color(),150)
        self.block.color = "0"
        self.assertEqual(self.block.get_color(),0)
    def test_colorrgba(self):
        self.block.color = "#200:200:150:20"
        self.assertEqual(self.block.get_color_as_rgba(),"#200:200:150:20")
        self.block.color = "200:200:150:20"
        self.assertEqual(self.block.get_color_as_rgba(),"rgba(200,200,150,20)")

    def test_properties(self):
        self.block.properties = [{"name": "time",
                            "label": "Time",
                            "lower": 0,
                            "upper": 10000,
                            "step": 1,
                            "value": 1
                            },
                            {"name": "color",
                            "label": "Color",
                            "value": "#F00",
                            "format": "FF00FF",
                            "type": MOSAICODE_COLOR
                            }
                           ]
        erro = {"erro": "time"}
        self.block.set_properties(erro)
