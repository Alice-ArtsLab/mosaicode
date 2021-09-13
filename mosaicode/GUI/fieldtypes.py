# -*- coding: utf-8 -*-
"""
This module contains the fieldtypes.
"""
from mosaicode.GUI.fields.checkfield import CheckField
from mosaicode.GUI.fields.colorfield import ColorField
from mosaicode.GUI.fields.combofield import ComboField
from mosaicode.GUI.fields.commentfield import CommentField
from mosaicode.GUI.fields.floatfield import FloatField
from mosaicode.GUI.fields.intfield import IntField
from mosaicode.GUI.fields.labelfield import LabelField
from mosaicode.GUI.fields.openfilefield import OpenFileField
from mosaicode.GUI.fields.savefilefield import SaveFileField
from mosaicode.GUI.fields.stringfield import StringField
from mosaicode.GUI.fields.charfield import CharField

MOSAICODE_CHECK = "Check"
MOSAICODE_CODE = "Code"
MOSAICODE_COLOR = "Color"
MOSAICODE_COMBO = "Combo"
MOSAICODE_COMMENT = "Comment"
MOSAICODE_FLOAT = "Float"
MOSAICODE_ICON = "Icon"
MOSAICODE_INT = "Int"
MOSAICODE_LABEL = "Label"
MOSAICODE_NONE = "None"
MOSAICODE_OPEN_FILE = "Open File"
MOSAICODE_SAVE_FILE = "Save File"
MOSAICODE_STRING = "String"
MOSAICODE_CHAR = "CHAR"

component_list = {
    MOSAICODE_CHECK: CheckField,
    MOSAICODE_COLOR: ColorField,
    MOSAICODE_COMBO: ComboField,
    MOSAICODE_COMMENT: CommentField,
    MOSAICODE_FLOAT: FloatField,
    MOSAICODE_INT: IntField,
    MOSAICODE_LABEL: LabelField,
    MOSAICODE_OPEN_FILE: OpenFileField,
    MOSAICODE_SAVE_FILE: SaveFileField,
    MOSAICODE_STRING: StringField,
    MOSAICODE_CHAR: CharField
}
