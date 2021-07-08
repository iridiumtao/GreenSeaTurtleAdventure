import pygame
import os, sys
import model
import random
from eventmanager import *
import src
import configparser
import os.path
from models import TurtleMC
from models import Straw
from models import Heart
from models import IntroObject
from models import MenuButton


backgroundColor = (93, 189, 245)
defaultColor = (255, 255, 255)

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """
        #pygame.init()
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallFont = None

        self.turtleCounter = 0
        self.introTextAlpha = 255

        self.menuButtonPos = (0, 0)
        self.tempNum = 0
        self.menuButtonState = 0


    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, InitializeEvent):
            self.initialize()

            self.backgroundImage = pygame.image.load("src/background.png").convert_alpha()
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, (self.windowWidth, self.windowHeight))


            # add intro page objects
            self.bigTurtle = IntroObject.IntroObject(self.windowWidth, self.windowHeight, w=858, h=672, x=-1000, y=150, stopX=-400, rate=8, turn=-15)
            self.bigStraw1 = IntroObject.IntroObject(self.windowWidth, self.windowHeight, w=200, h=700, x=1100, y=390, stopX=900, rate=-8, turn=-60, flip=True, image="src/straw.png")
            self.bigStraw2 = IntroObject.IntroObject(self.windowWidth, self.windowHeight, w=200, h=700, x=1100, y=350, stopX=950, rate=-8, turn=-50, flip=True, image="src/straw.png")
            self.bigStraw3 = IntroObject.IntroObject(self.windowWidth, self.windowHeight, w=200, h=700, x=1100, y=300, stopX=900, rate=-8, turn=-40, flip=True, image="src/straw.png")

            # 生成 menu 按鈕
            self.menuContiuneButton = MenuButton.MenuButton(x = self.windowWidth * 0.275,
                                                            y = self.windowHeight * 0.235,
                                                            w = self.windowWidth * 0.45,
                                                            h = self.windowHeight * 0.135,
                                                            image = "src/continue-button.png")
            self.menuNewGameButton = MenuButton.MenuButton(x = self.windowWidth * 0.275,
                                                           y = self.windowHeight * 0.42,
                                                           w = self.windowWidth * 0.45,
                                                           h = self.windowHeight * 0.135,
                                                           image = "src/start-button.png")
            self.menuOptionButton = MenuButton.MenuButton(x = self.windowWidth * 0.275,
                                                          y = self.windowHeight * 0.605,
                                                          w = self.windowWidth * 0.21,
                                                          h = self.windowHeight * 0.135,
                                                          image = "src/option-button.png")
            self.menuHelpButton = MenuButton.MenuButton(x = self.windowWidth * 0.515,
                                                        y = self.windowHeight * 0.605,
                                                        w = self.windowWidth * 0.21,
                                                        h = self.windowHeight * 0.135,
                                                        image = "src/help-button.png")

            self.menuButtons = pygame.sprite.Group((self.menuContiuneButton,) +
                                                   (self.menuNewGameButton,) +
                                                   (self.menuOptionButton,) +
                                                   (self.menuHelpButton,))


            # 生成海龜
            self.creatures = pygame.sprite.Group()
            self.creature = TurtleMC.TurtleMC(1/5, self.windowWidth, self.windowHeight)
            self.creatures.add(self.creature)

            # 生成吸管
            self.straws = pygame.sprite.Group()
            strawNum = 20
            for i in range(strawNum):
                self.straws.add(Straw.Straw(self.windowWidth, random.randint(self.windowWidth, self.windowWidth*2), (self.windowHeight/strawNum)*i+10))

            # 生成心臟
            self.hearts = pygame.sprite.Group()
            heartNum = 2
            heartSize = 52
            for i in range(heartNum):
                self.hearts.add(Heart.Heart(0 + i * heartSize, self.windowHeight - heartSize, heartSize))

        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
             # Called for each game tick. We check our keyboard presses here.
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_INTRO:
                self.renderIntro()
            if currentstate == model.STATE_MENU:
                self.renderMenu(event)
            if currentstate == model.STATE_PLAY:
                self.renderPlay()
            if currentstate == model.STATE_HELP:
                self.renderHelp()

            # 鍵盤上下左右的狀態
            if currentstate == model.STATE_RIGHT:
                self.renderRight()
            if currentstate == model.STATE_LEFT:
                self.renderLeft()
            if currentstate == model.STATE_UP:
                self.renderUp()
            if currentstate == model.STATE_DOWN:
                self.renderDown()

            # 設定 60 FPS
            self.clock.tick(60)

        elif isinstance(event, InputEvent):
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_MENU:
                self.menuButtonPos = event.clickpos

    def renderIntro(self):
        self.screen.fill(defaultColor)
        self.screen.fill(backgroundColor)
        self.screen.blit(self.backgroundImage, (0, 0))

        text = self.smallFont.render(
                    'Press space key to start.',
                    True, (0, 0, 0))


        # 把海龜跟吸管弄進來
        self.introObj = pygame.sprite.Group((self.bigTurtle,) + (self.bigStraw1,) + (self.bigStraw2,) + (self.bigStraw3,))
        self.introObj.draw(self.screen)
        for i in self.introObj:
            i.update()

        # 讓 intro text 有呼吸效果
        self.introTextAlpha = self.introTextAlpha - 4 if self.introTextAlpha > -255 else 255
        text.set_alpha(abs(self.introTextAlpha))

        # 計算文字位置，水平置中、垂直0.8
        text_rect = text.get_rect(center = (self.windowWidth / 2, self.windowHeight * 0.8))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def renderMenu(self, event):
        """
        Render the game menu.
        """

        self.screen.fill(backgroundColor)

        self.screen.blit(self.backgroundImage, (0, 0))

        self.menuButtons.draw(self.screen)
        for i in self.menuButtons:
            i.update()

        # 偵測是否有按下滑鼠，並判斷是否在按鈕的範圍內
        if self.menuContiuneButton.rect.collidepoint(self.menuButtonPos):
            # todo: 顯示一個更大的 button，讓它看起來有跳起來的感覺
            print("按下「繼續遊戲」")
            self.evManager.Post(MenuButtonEvent(model.MENU_CONTIUNE))
            self.menuButtonPos = (0, 0)

        # 新遊戲
        if self.menuNewGameButton.rect.collidepoint(self.menuButtonPos):
            print("按下「新遊戲」")
            self.evManager.Post(MenuButtonEvent(model.MENU_NEW_GAME))
            self.menuButtonPos = (0, 0)

        # 選項
        if self.menuOptionButton.rect.collidepoint(self.menuButtonPos):
            print("按下「選項」")
            self.evManager.Post(MenuButtonEvent(model.MENU_OPTION))
            self.menuButtonPos = (0, 0)

        # 說明
        if self.menuHelpButton.rect.collidepoint(self.menuButtonPos):
            print("按下「說明」")
            self.evManager.Post(MenuButtonEvent(model.MENU_HELP))
            self.menuButtonPos = (0, 0)

        pygame.display.flip()

    def renderPlay(self):
        """
        Render the game play.
        """
        self.refresh()

    def renderHelp(self):
        """
        Render the help screen.
        """

        self.screen.fill(backgroundColor)
        somewords = self.smallFont.render(
                    'Help is here. space, escape or return. 中文字測試',
                    True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()

    def renderRight(self):
        """
        角色向右移動
        """
        self.creature.move("right")
        self.refresh()

    def renderLeft(self):
        """
        角色向左移動
        """
        self.creature.move("left")
        self.refresh()

    def renderUp(self):
        """
        角色向上移動
        """
        self.creature.move("up")
        self.refresh()

    def renderDown(self):
        """
        角色向下移動
        """
        self.creature.move("down")
        self.refresh()

    def refresh(self):
        """
        刷新畫面上顯示的內容
        """
        self.screen.fill(backgroundColor)

        self.screen.blit(self.backgroundImage, (0, 0))

        somewords = self.smallFont.render('You are Playing the game. F1 for help.', True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        self.creatures.update()
        self.creatures.draw(self.screen)
        self.straws.update()
        self.straws.draw(self.screen)
        self.hearts.update()
        self.hearts.draw(self.screen)

        # score counter
        self.turtleCounter += 1
        score = self.smallFont.render(str(self.turtleCounter // 6), False, (0, 0, 0))
        score_rect = score.get_rect(topright = (self.windowWidth , 0))
        self.screen.blit(score, score_rect)

        # 顯示hitBox
        pygame.draw.rect(self.screen, (255, 0, 0), self.creature.hitBox.rect, 2)
        # print(pygame.sprite.spritecollide(self.creature.hitBox, self.straws, False))

        pygame.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        if not os.path.isfile('config.ini'):
            resolutionWidth = 1280
            resolutionHeight = 720
            screenFlags = pygame.SCALED
            displayIndex = 0
            vsync = 1
            self.generateConfig()
        else:
            resolutionWidth, resolutionHeight, screenFlags, displayIndex, vsync = self.applyConfig()

        result = pygame.init()
        pygame.init()
        pygame.font.init()
        #pygame.display.init()
        pygame.display.set_caption('Green Sea Turtle Adventure')
        self.screen = pygame.display.set_mode((resolutionWidth, resolutionHeight),
                                                screenFlags,
                                                display = displayIndex,
                                                vsync = vsync)
        self.windowWidth, self.windowHeight = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.smallFont = pygame.font.Font("src/jf-openhuninn-1.1.ttf", 40)
        self.isinitialized = True

    def generateConfig(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config['SCREEN'] = {'RESOLUTION_WIDTH' : '1280',
                            'RESOLUTION_HEIGHT' : '720',
                            '# 將全螢幕設為TRUE可能會造成系統解析度的問題' : None,
                            '# Set fullscreen to TRUE may cause some problem on system resolution.' : None,
                            'FULLSCREEN' : 'FALSE',
                            'SCALED' : 'TRUE',
                            'NOFRAME' : 'FALSE',
                            'OPENGL' : 'FALSE',
                            'display_index' : '0',
                            '# 需要開啟OPENGL或SCALED使VSYNC有效' : None,
                            '# VSYNC only works with the OPENGL or SCALED flags set TRUE' : None,
                            'vsync' : '1'}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def applyConfig(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')

            screen = config['SCREEN']

            resolutionWidth = int(screen['resolution_width'])
            resolutionHeight = int(screen['resolution_height'])
            screenFlags = 0
            if screen.getboolean('fullscreen'):
                screenFlags = pygame.FULLSCREEN
            if screen.getboolean('scaled'):
                screenFlags = screenFlags | pygame.SCALED
            if screen.getboolean('noframe'):
                screenFlags = screenFlags | pygame.NOFRAME
            if screen.getboolean('opengl'):
                screenFlags = screenFlags | pygame.OPENGL
            display_index = int(screen['display_index'])
            vsync = int(screen['vsync'])
            return resolutionWidth, resolutionHeight, screenFlags, display_index, vsync
        except:
            self.generateConfig()
            return 1280, 720, pygame.SCALED, 0, 1
