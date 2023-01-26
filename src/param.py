from src.util import logPrint

TIME_TOLERANCE = (0, 0.1)
LOG_MUTE_LEVEL = -1
WINDOW_TITLE = '《战舰世界》'
WINDOW_MODE = 'FS'
WINDOW_SIZE = (700, 500)
WINDOW_POSITION = (0, 0)
DISPLAY_RESOLUTION = (1920, 1080)

origin = (1, 0)

def calibrateOrigin(newOrigin):
    global origin
    origin = (newOrigin[0], newOrigin[1])
    logPrint(2, "[Note] Origin reset at", origin)

# All positions below are relative position.

class Region:

    def __init__(self, topleft_x, topleft_y, bottomright_x, bottomright_y):
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.bottomright_x = bottomright_x
        self.bottomright_y = bottomright_y

    def center(self):
        return (self.topleft_x + self.bottomright_x) / 2, (self.topleft_y + self.bottomright_y) / 2

    def toAbsoluteRegionCoordinate(self, region):
        # return coordinates of upper-left point and lower-right point.
        return region.topleft_x + origin.x, region.topleft_y + origin.y, \
               region.bottomright_x + origin.x, region.bottomright_y + origin.y


# Following coordinates are based on game process origin (0,0), need to convert to absolute coordinates.
HOME_IDENTIFY_REGION = Region(1178, 0, 1384, 70)
SEARCHING_IDENTIFY_REGION = Region(1199, 1138, 1352, 1273)
GAME_COMPLETE_IDENTIFY_REGION = Region(1967, 1305, 2151, 1345)

# todo: frontier of dev
COMPT_MODE_BUTTON_POSITION = (350, 175)
BRAWL_MODE_BUTTON_POSITION = (350, 240)
START_GAME_BUTTON_POSITION = (538, 412)
START_BRAWL_BUTTON_POSITION = (593, 382)
END_TURN_BUTTON_POSITION = (600, 244)
CASUAL_MODE_BUTTON_POSITION = (491, 108)
SOMEWHERE_POSITION = (673, 45)
DECK_1_BUTTON_POSITION = (149, 161)
X_BETWEEN_DECK = 100
Y_BETWEEN_DECK = 90
NEXT_DECK_PAGE_BUTTON_POSITION = (422, 256)
PREV_DECK_PAGE_BUTTON_POSITION = (67, 256)
FINISH_SHUFFLE_BUTTON_POSITION = (350, 398)
HERO_POWER_BUTTON_POSITION = (437, 395)
SHUFFLE_IDENTIFY_REGION = (316, 377, 75, 41)
RESULT_IDENTIFY_REGION = (308, 280, 85, 55)
SEARCHING_IDENTIFY_REGION = (246, 97, 214, 49)
ERROR_01_IDENTIFY_REGION = (311, 210, 73, 19)
ERROR_02_IDENTIFY_REGION = (272, 222, 144, 70)
ERROR_03_IDENTIFY_REGION = (317, 126, 69, 33)
END_TURN_BUTTON_REGION = (567, 229, 62, 29)
SETTING_BUTTON_POSITION = (671, 479)
SURRENDER_BUTTON_POSITION = (350, 198)
ERROR_01_BUTTON_POSITION = (347, 306)
ERROR_03_BUTTON_POSITION = (285, 378)
GAME_LAUNCHER_POSITION = (290, 1043)
GAME_LAUNCHER_BUTTON_POSITION = (213, 969)
