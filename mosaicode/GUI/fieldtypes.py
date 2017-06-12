# -*- coding: utf-8 -*-
"""
This module contains the fieldtypes.
"""
from mosaicode.GUI.components.checkfield import CheckField
from mosaicode.GUI.components.colorfield import ColorField
from mosaicode.GUI.components.combofield import ComboField
from mosaicode.GUI.components.commentfield import CommentField
from mosaicode.GUI.components.floatfield import FloatField
from mosaicode.GUI.components.iconfield import IconField
from mosaicode.GUI.components.intfield import IntField
from mosaicode.GUI.components.openfilefield import OpenFileField
from mosaicode.GUI.components.savefilefield import SaveFileField
from mosaicode.GUI.components.stringfield import StringField

MOSAICODE_CHECK = "Check"
MOSAICODE_CODE = "Code"
MOSAICODE_COLOR = "Color"
MOSAICODE_COMBO = "Combo"
MOSAICODE_COMMENT = "Comment"
MOSAICODE_FLOAT = "Float"
MOSAICODE_ICON = "Icon"
MOSAICODE_INT = "Int"
MOSAICODE_NONE = "None"
MOSAICODE_OPEN_FILE = "Open File"
MOSAICODE_SAVE_FILE = "Save File"
MOSAICODE_STRING = "String"

component_list = {
    MOSAICODE_CHECK: CheckField,
    MOSAICODE_COLOR: ColorField,
    MOSAICODE_COMBO: ComboField,
    MOSAICODE_COMMENT: CommentField,
    MOSAICODE_FLOAT: FloatField,
    MOSAICODE_ICON: IconField,
    MOSAICODE_INT: IntField,
    MOSAICODE_OPEN_FILE: OpenFileField,
    MOSAICODE_SAVE_FILE: SaveFileField,
    MOSAICODE_STRING: StringField
}
