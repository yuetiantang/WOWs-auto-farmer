from src.param import *
import numpy
import cv2
import api
import pyautogui
import pygetwindow
import time
import random


origin = pygetwindow.Point(0, 0)


def sleep(sec):
    time.sleep(sec + random.uniform(TIME_TOLERANCE[0], TIME_TOLERANCE[1]))


def logPrint(level=0, *args):
    if level > LOG_MUTE_LEVEL:
        print(time.asctime(), ':', *args)


def pause(sec):
    logPrint(2, 'Info: Script paused for', sec, 'seconds.')
    sleep(sec)
    logPrint(2, 'Info: Script resumed.')


def toRelPosition(absX, absY):
    return absX - origin.x, absY - origin.y


def toAbsPosition(relX, relY):
    return relX + origin.x, relY + origin.y


def toAbsBox(relBox):
    # return coordinates of upper-left point and lower-right point.
    return relBox[0] + origin.x, relBox[1] + origin.y, relBox[2] + origin.x, relBox[3] + origin.y


def getMouseAbsPosition():
    return pyautogui.position().x, pyautogui.position().y


def getMouseRelPosition():
    temp = getMouseAbsPosition()
    return toRelPosition(temp[0], temp[1])

def getGameWindow(numAttempts=5):
    window = pygetwindow.getWindowsWithTitle(WINDOW_TITLE)
    currNumAttempts = 0
    while len(window) != 1:
        currNumAttempts += 1
        if currNumAttempts > numAttempts:
            return None
        if len(window) == 0:
            logPrint(4, "Error: Cannot locate game progress. Reattempt in 5 seconds." +
                        "[{currNumAttempts}/{numAttempts}]".format(currNumAttempts=currNumAttempts, numAttempts=numAttempts))
        if len(window) > 1:
            logPrint(4, "Error: Multiple game programs detected. Reattempt in 5 seconds.")
        sleep(5)
        window = pygetwindow.getWindowsWithTitle(WINDOW_TITLE)
    window = window[0]
    logPrint(1, "Game window captured.")
    if WINDOW_MODE == 'FS':
        try:
            window.activate()
        except pygetwindow.PyGetWindowException:
            logPrint(2, 'Info: Multiple monitor detected.')
    elif WINDOW_MODE == '2560-1440':
        window.resizeTo(WINDOW_SIZE[0], WINDOW_SIZE[1])
        window.activate()
        window.moveTo(WINDOW_POSITION[0], WINDOW_POSITION[1])
    return window.topleft


def click(position):
    x = pyautogui.position().x
    y = pyautogui.position().y
    pyautogui.click(toAbsPosition(position[0], position[1]))
    sleep(0.1)
    pyautogui.moveTo(x, y)


def clickBattle():
    click(HOME_IDENTIFY_REGION.center())


def clickComptMode():
    click(COMPT_MODE_BUTTON_POSITION)


def clickBrawlMode():
    click(BRAWL_MODE_BUTTON_POSITION)


def clickOnNextPage():
    click(NEXT_DECK_PAGE_BUTTON_POSITION)


def clickStartGame():
    click(START_GAME_BUTTON_POSITION)


def clickStartBrawl():
    click(START_BRAWL_BUTTON_POSITION)


def clickOnPreviousPage():
    click(PREV_DECK_PAGE_BUTTON_POSITION)


def clickEndTurn():
    click(END_TURN_BUTTON_POSITION)


def clickHeroPower():
    click(HERO_POWER_BUTTON_POSITION)


def clickOnDeck(num):
    deck = num
    if deck > 9:
        clickOnNextPage()
        deck -= 9
    else:
        clickOnPreviousPage()
    sleep(0.5)
    click((DECK_1_BUTTON_POSITION[0] + (deck - 1) % 3 * X_BETWEEN_DECK, \
           DECK_1_BUTTON_POSITION[1] + (deck - 1) // 3 * Y_BETWEEN_DECK))


def clickCasualMode():  # outdated
    click(CASUAL_MODE_BUTTON_POSITION)


def clickFinishShuffling():
    click(FINISH_SHUFFLE_BUTTON_POSITION)


def clickSomewhere():
    click(SOMEWHERE_POSITION)


def clickSetting():
    click(SETTING_BUTTON_POSITION)


def clickSurrender():
    clickSetting()
    click(SURRENDER_BUTTON_POSITION)


def clickDismissError01():
    click(ERROR_01_BUTTON_POSITION)


def clickDismissError03():
    click(ERROR_03_BUTTON_POSITION)
    sleep(0.5)
    click((ERROR_03_BUTTON_POSITION[0] + 30, \
           ERROR_03_BUTTON_POSITION[1]))


def clickLaunchGame_01():
    click(GAME_LAUNCHER_POSITION)


def clickLaunchGame_02():
    click(GAME_LAUNCHER_BUTTON_POSITION)


def findPngOnScreen(pngName, box, sim):
    if pyautogui.locateOnScreen(pngName + '.png', region=box, confidence=sim):
        return True
    else:
        return False

# todo
def isHome():
    return findPngOnScreen('../images/battle-bar', toAbsBox(HOME_IDENTIFY_REGION), 0.5)


def isDefeat():
    return findPngOnScreen('../images/defeat', toAbsBox(RESULT_IDENTIFY_REGION), 0.5)


def isWin():
    return findPngOnScreen('../images/win', toAbsBox(RESULT_IDENTIFY_REGION), 0.5)


def isEndOfGame():
    return isWin() or isDefeat()


def isError01():
    return findPngOnScreen('../images/error_01', toAbsBox(ERROR_01_IDENTIFY_REGION), 0.8)


def isError02():
    return findPngOnScreen('../images/error_02', toAbsBox(ERROR_02_IDENTIFY_REGION), 0.8)


def isError03():
    return findPngOnScreen('../images/error_03', toAbsBox(ERROR_03_IDENTIFY_REGION), 0.8)


def isShuffling():
    return findPngOnScreen('../images/shuffling', toAbsBox(SHUFFLE_IDENTIFY_REGION), 0.8)


def isSearching():
    return findPngOnScreen('../images/searching', toAbsBox(SEARCHING_IDENTIFY_REGION), 0.8)


def shouldEndTurn():
    return findPngOnScreen('../images/shouldEndTurn', toAbsBox(END_TURN_BUTTON_REGION), 0.9)


def shouldPlay():
    return findPngOnScreen('../images/shouldPlay', toAbsBox(END_TURN_BUTTON_REGION), 0.5)


def notMyTurn():
    return findPngOnScreen('../images/notMyTurn', toAbsBox(END_TURN_BUTTON_REGION), 0.5)


def isPlaying():
    return (not isEndOfGame()) and (shouldPlay() or shouldEndTurn() or notMyTurn())
