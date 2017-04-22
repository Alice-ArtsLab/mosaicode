# -*- coding: utf-8 -*-
"""
This module contains the fieldtypes.
"""
from harpia.GUI.components.checkfield import CheckField
from harpia.GUI.components.colorfield import ColorField
from harpia.GUI.components.combofield import ComboField
from harpia.GUI.components.commentfield import CommentField
from harpia.GUI.components.floatfield import FloatField
from harpia.GUI.components.iconfield import IconField
from harpia.GUI.components.intfield import IntField
from harpia.GUI.components.openfilefield import OpenFileField
from harpia.GUI.components.savefilefield import SaveFileField
from harpia.GUI.components.stringfield import StringField

HARPIA_CHECK = "Check"
HARPIA_CODE = "Code"
HARPIA_COLOR = "Color"
HARPIA_COMBO = "Combo"
HARPIA_COMMENT = "Comment"
HARPIA_FLOAT = "Float"
HARPIA_ICON = "Icon"
HARPIA_INT = "Int"
HARPIA_NONE = "None"
HARPIA_OPEN_FILE = "Open File"
HARPIA_SAVE_FILE = "Save File"
HARPIA_STRING = "String"

component_list = {
    HARPIA_CHECK: CheckField,
    HARPIA_COLOR: ColorField,
    HARPIA_COMBO: ComboField,
    HARPIA_COMMENT: CommentField,
    HARPIA_FLOAT: FloatField,
    HARPIA_ICON: IconField,
    HARPIA_INT: IntField,
    HARPIA_OPEN_FILE: OpenFileField,
    HARPIA_SAVE_FILE: SaveFileField,
    HARPIA_STRING: StringField
}
