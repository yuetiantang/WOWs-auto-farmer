# from PIL import imageGrab
import sys

from src.util import *
from src.param import *



win = 0
lose = 0
reconnect = 0

pyautogui.FAILSAFE = False


# -------- Utils -------- #


# ---- In-Game Operations ---- #
def endTurn():
    # call iff game is in progress! #
    if shouldEndTurn() or shouldPlay():
        clickEndTurn()
    elif notMyTurn():
        return
    elif isEndOfGame():
        return
    else:
        sleep(1)
        endTurn()


def useHeroPower():
    clickHeroPower()


# -------- Strategies -------- #
def strategy_ComptHunter():
    useHeroPower()
    endTurn()


def strategy_UsePower():
    useHeroPower()


def strategy_AFK():
    # endTurn()
    return


def strategy_ShootThenGiveUp():
    clickHeroPower()
    clickSurrender()


def strategy_IGiveUp():
    clickSurrender()


# -------- Commands -------- #
def init(timeout=5):
    logPrint(1, "Script initializing...")
    origin = getGameWindow(timeout)
    if origin is None:
        return False
    calibrateOrigin(origin)
    return True


def startCoopFromHome():
    logPrint(1, "5 seconds before initialization...")
    sleep(5)
    logPrint(1, "Initialization starts.")
    if not init():
        logPrint(5, 'FATAL: [0-0] Failed to capture game window')
        return
    # todo: Frontier of dev
    while True:
        if isHome():
            clickBattle()
        else:
            logPrint(3, "[WARNING] Cannot start battle because game is not in the home page.")
    return
    # todo: check main menu.

    sleep(4)
    clickOnDeck(deck)
    sleep(1)
    # clickCasualMode() # outdated
    logPrint(1, "Initialization done.")
    if grind(strategy, 999999) == 'E-02':
        autoReconnect()
    logPrint(5, "Fatal: [E-05] Script has touched the end.")
    return


def autoBrawl(deck, strategy):
    # beta
    init()
    clickBrawlMode()
    sleep(1)
    clickStartBrawl()
    if deck:
        clickOnDeck(deck)
    else:
        ""
    brawlGrind(strategy, 999999)


def brawlGrind(strategy, num):
    # beta
    for cycle in range(0, num):
        while not isSearching():
            clickStartBrawl()
        sleep(2)
        while isSearching():
            logPrint('matching...')
            time.sleep(5)
        while not isShuffling():
            clickStartBrawl()
            time.sleep(5)
        startPlay(strategy)


def grind(strategy, num):
    for cycle in range(0, num):
        clickOnDeck(DECK)
        sleep(1)
        clickStartGame()
        logPrint(1, "Searching for a worthy opponent...")
        sleep(1)
        while not isSearching():
            if isError01():
                logPrint(4,
                         'Error: [E-01] Cannot start game, probably because of a connection error. Try restart searching.')
                clickDismissError01()
                sleep(1)
                continue
            elif isError03():
                logPrint(4, 'Error: [E-03] Connection Error. Reconnecting...')
                clickDismissError03()
                sleep(1)
                continue
            else:
                logPrint(1, 'Searching interrupted. Restart searching...')
                clickOnDeck(DECK)
                sleep(1)
                clickStartGame()
                sleep(2)
        sleep(1)
        while isSearching():
            logPrint(1, 'Searching...')
            sleep(10)
        logPrint(2, 'Search ends.')
        sleep(5)
        if isError01():
            logPrint(4,
                     'Error: [E-01] Cannot start game, probably because of a connection error. Try restart searching.')
            clickDismissError01()
            sleep(1)
            continue
        if isError02():
            logPrint(5, 'Fatal: [E-02] Disconnected. Game crashed.')
            clickSomewhere()
            sleep(5)
            logPrint(2, 'Script terminated.')
            return 'E-02'
        elif isError03():
            logPrint(4, 'Error: [E-03] Connection Error. Try reconnection.')
            clickDismissError03()
            sleep(1)
            continue
        logPrint(2, 'Found a worthy opponent. Game will start soon.')
        if startPlay(strategy) == 'E-02':
            return 'E-02'


def startPlay(strategy):
    global win, lose

    def checkEndOfGame():
        if isEndOfGame():
            global win, lose
            result = '?'
            checkCounter = 0
            checkLimit = 5
            while result == '?' and checkCounter < checkLimit:
                if isDefeat():
                    lose += 1
                    result = 'LOSE.'
                elif isWin():
                    win += 1
                    result = 'WIN.'
                checkCounter += 1
            logPrint(2, 'Game ends with a', result)
            logPrint(2, 'Current record: WIN:', win, 'LOSE:', lose, 'Reconnect:', reconnect)
            clickSomewhere()
            return True
        logPrint(3, 'Warning: Fail to check the end of game.')
        return False

    if isEndOfGame():
        "Early Game End."
        logPrint(3, 'Warning: Early Game End detected, possibly due to an instant surrender from the opponent.')
        if checkEndOfGame():
            return
    while not isShuffling():
        "Wait for screen to update."
        logPrint(2, 'Info: Waiting for hand confirmation panel...')
        sleep(10)
        if isEndOfGame():
            logPrint(2, 'Info: This game ends before hand confirmation.')
            if checkEndOfGame():
                return
    while isShuffling():
        # TODO: shuffling strategy not implemented.
        clickFinishShuffling()
        logPrint(2, 'Hand confirmed.')
        sleep(1)
    logPrint(2, 'Game started.')
    clickCount = 0
    clickLimit = 40

    # 15
    hasClicked = False
    while not isEndOfGame():
        "Now game start. Keep updating."
        if notMyTurn():
            "Disabled"
            logPrint(0, 'Game in progress. Opponent\'s turn.')
            hasClicked = False
            sleep(3)
        elif shouldEndTurn():
            "Disabled"
            logPrint(0, 'Game in progress. Player\'s turn. AFKing.')
            hasClicked = True
            # clickEndTurn()
            sleep(6)
        elif shouldPlay():
            if not hasClicked:
                logPrint(0, 'Game in progress. Player\'s turn. Using strategy.')
                strategy()
                hasClicked = True
                clickCount += 1
                sleep(10)
            else:
                logPrint(0, 'Game in progress. Player\'s turn. Opt-AFKing.')
                sleep(1)
                if clickCount >= clickLimit:
                    logPrint(2, "Info: Reached idle-maximum. Surrendered.")
                    clickSurrender()
                    sleep(8)
        else:
            logPrint(0, 'Cannot determine game stage. Game still in progress.')
            if isError02():
                logPrint(5, 'Fatal: [E-02] Disconnected. Game crashed.')
                clickSomewhere()
                sleep(5)
                logPrint(2, 'Script terminated.')
                return 'E-02'
            sleep(3)
    endCheckTimer = 0
    endCheckLimit = 5
    while isEndOfGame():
        if checkEndOfGame():
            logPrint(2, 'Game normally ends.')
            return
        endCheckTimer += 1
        sleep(3)
        if endCheckTimer >= endCheckLimit:
            logPrint(4, "Error: [E-04] Game End-check failed. Game abnormally ends.")
            return


def trackMouse(limit, game='off'):
    i = 0
    if game is not 'off':
        init()
    while True:
        print(getMouseRelPosition())
        time.sleep(1)
        i += 1
        if i > limit:
            break


def test(func):
    i = 0
    init()
    while True:
        print(func())
        time.sleep(1)
        i += 1
        if i > 9999:
            break


# ----------- PARAM ---------- #
LOG_MUTE_LEVEL = 0
DECK = 1
# ----------- Main ----------- #


win = 0
lose = 0
gold = 10110
xp = 453 / 1500
stage = 155
dust = 10180 + 4100
level = 4939 / 5224 / 5368
# ------------------ #
gold2 = 1620
level2 = 0 / 1 / 6883
# ---------------------------- #
if len(sys.argv) > 1 and int(sys.argv[1]):
    DECK = int(sys.argv[1])
startCoopFromHome()  # SFW
# autoMatch(8, strategy_AFK)
# test(shouldEndTurn)
trackMouse(9999)
