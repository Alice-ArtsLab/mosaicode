# -*- coding: utf-8 -*-

from harpia.GUI.components.intfield import IntField
from harpia.GUI.components.checkfield import CheckField
from harpia.GUI.components.colorfield import ColorField
from harpia.GUI.components.combofield import ComboField
from harpia.GUI.components.floatfield import FloatField
from harpia.GUI.components.stringfield import StringField
from harpia.GUI.components.commentfield import CommentField
from harpia.GUI.components.openfilefield import OpenFileField
from harpia.GUI.components.savefilefield import SaveFileField

HARPIA_NONE = "None"
HARPIA_STRING = "String"
HARPIA_COMMENT = "Comment"
HARPIA_CODE = "Code"
HARPIA_INT = "Int"
HARPIA_COLOR = "Color"
HARPIA_FLOAT = "Float"
HARPIA_SAVE_FILE = "Save"
HARPIA_OPEN_FILE = "Open"
HARPIA_COMBO = "Combo"
HARPIA_CHECK = "Check"

component_list = {
    HARPIA_INT: IntField,
    HARPIA_CHECK: CheckField,
    HARPIA_COLOR: ColorField,
    HARPIA_COMBO: ComboField,
    HARPIA_FLOAT: FloatField,
    HARPIA_STRING: StringField,
    HARPIA_COMMENT: CommentField,
    HARPIA_OPEN_FILE: OpenFileField,
    HARPIA_SAVE_FILE: SaveFileField
}
