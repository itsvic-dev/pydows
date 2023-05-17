from enum import Enum


class HoloMDL2IconMap(Enum):
    WINDOWS = "\ue782"


class SegoeMDL2IconMap(Enum):
    SEARCH = "\ue721"
    TASK_VIEW = "\ue7c4"
    ACTION_CENTER_NOTIFICATION = "\ue7e7"
    ETHERNET = "\ue839"
    ACTION_CENTER = "\ue91c"
    CHEVRON_UP_MED = "\ue971"
    VOLUME_0 = "\ue992"
    VOLUME_1 = "\ue993"
    VOLUME_2 = "\ue994"
    VOLUME_3 = "\ue995"


class AcrylicColors(Enum):
    TASKBAR = (31, 31, 31, 192)


class Font(Enum):
    SEGOE_UI = "segoeui"
    SEGOE_UI_BOLD = "segoeuib"
    SEGOE_UI_SEMIBOLD = "seguisb"
    SEGOE_MDL2 = "segmdl2"
    HOLOLENS_MDL2 = "holomdl2"


class Duration(Enum):
    NOTIFICATION_SLIDE = 0.8
