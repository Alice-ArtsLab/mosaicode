# -*- coding: utf-8 -*-
"""
This module contains the fieldtypes.
"""
from mosaicomponents.checkfield import CheckField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.combofield import ComboField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.floatfield import FloatField
from mosaicomponents.iconfield import IconField
from mosaicomponents.intfield import IntField
from mosaicomponents.openfilefield import OpenFileField
from mosaicomponents.savefilefield import SaveFileField
from mosaicomponents.stringfield import StringField

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
