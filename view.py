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


BACKGROUND_BLUE = (93, 189, 245)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = None
WINDOW_WIDTH = None

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
        self.smallfont = None

        self.turtleCounter = 0
        self.intro_text_alpha = 255

        self.menuButtonPos = (0, 0)
        self.tempNum = 0


    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, InitializeEvent):
            self.initialize()

            self.background_image = pygame.image.load("src/background.png").convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))


            # add intro page objects
            self.bigTurtle = IntroObject.IntroObject(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, w=858, h=672, x=-1000, y=150, stopX=-400, rate=8, turn=-15)
            self.bigStraw1 = IntroObject.IntroObject(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, w=200, h=700, x=1100, y=390, stopX=900, rate=-8, turn=-60, flip=True, image="src/straw.png")
            self.bigStraw2 = IntroObject.IntroObject(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, w=200, h=700, x=1100, y=350, stopX=950, rate=-8, turn=-50, flip=True, image="src/straw.png")
            self.bigStraw3 = IntroObject.IntroObject(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, w=200, h=700, x=1100, y=300, stopX=900, rate=-8, turn=-40, flip=True, image="src/straw.png")

            # add turtle object

            # 生成海龜
            self.creatures = pygame.sprite.Group()
            self.creature = TurtleMC.TurtleMC(1/5, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
            self.creatures.add(self.creature)

            # 生成吸管
            self.straws = pygame.sprite.Group()
            strawNum = 20
            for i in range(strawNum):
                self.straws.add(Straw.Straw(self.WINDOW_WIDTH, random.randint(self.WINDOW_WIDTH, self.WINDOW_WIDTH*2), (self.WINDOW_HEIGHT/strawNum)*i+10))

            # 生成心臟
            self.hearts = pygame.sprite.Group()
            heartNum = 2
            heartSize = 52
            for i in range(heartNum):
                self.hearts.add(Heart.Heart(0 + i * heartSize, self.WINDOW_HEIGHT - heartSize, heartSize))

        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_INTRO:
                self.renderintro()
            if currentstate == model.STATE_MENU:
                self.rendermenu(event)
            if currentstate == model.STATE_PLAY:
                self.renderplay()
            if currentstate == model.STATE_HELP:
                self.renderhelp()

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

    def renderintro(self):
        self.screen.fill(WHITE)
        self.screen.fill(BACKGROUND_BLUE)
        self.screen.blit(self.background_image, (0, 0))

        text = self.smallfont.render(
                    'Press space key to start.',
                    True, (0, 0, 0))


        # 把海龜跟吸管弄進來
        self.introObj = pygame.sprite.Group((self.bigTurtle,) + (self.bigStraw1,) + (self.bigStraw2,) + (self.bigStraw3,))
        self.introObj.draw(self.screen)
        for i in self.introObj:
            i.update()

        # 讓 intro text 有呼吸效果
        self.intro_text_alpha = self.intro_text_alpha - 4 if self.intro_text_alpha > -255 else 255
        text.set_alpha(abs(self.intro_text_alpha))

        # 計算文字位置，水平置中、垂直0.8
        text_rect = text.get_rect(center = (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.8))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def rendermenu(self, event):
        """
        Render the game menu.
        """

        """
        todo:
        1. 繼續遊戲
        2. 新遊戲
        3. 選項
        4. 幫助

        """
        self.screen.fill(BACKGROUND_BLUE)

        self.screen.blit(self.background_image, (0, 0))



        # self.smallfont.render(text, antialias, color, background=None) -> Surface
        titleText = self.smallfont.render(
                    'You are in the Menu. Space to play. Esc exits.',
                    True, (0, 0, 0))
        self.screen.blit(titleText, (0, 0))
        displaySettingText = self.smallfont.render(
                    'Resolution:',
                    True, (0, 0, 0))
        displaySettingText2 = self.smallfont.render(
                    '1920x1080',
                    True, (0, 0, 0))
        displaySettingText3 = self.smallfont.render(
                    '1366x768',
                    True, (0, 0, 0))
        displaySettingText4 = self.smallfont.render(
                    '3840x2160',
                    True, (0, 0, 0))
        self.screen.blit(displaySettingText, (0, 40))
        self.screen.blit(displaySettingText2, (40, 80))
        self.screen.blit(displaySettingText3, (40, 120))
        self.screen.blit(displaySettingText4, (40, 160))

        # 偵測是否有按下滑鼠，並判斷是否在按鈕的範圍內
        mouse_x, mouse_y = self.menuButtonPos
        if mouse_x > self.WINDOW_WIDTH * 0.34 and mouse_x < self.WINDOW_WIDTH * 0.66:

            # 繼續遊戲
            if mouse_y > self.WINDOW_HEIGHT * 0.235 and mouse_y < self.WINDOW_HEIGHT * 0.37:
                print("按下「繼續遊戲」")
                self.menuButtonPos = (0, 0)

            # 新遊戲
            if mouse_y > self.WINDOW_HEIGHT * 0.42 and mouse_y < self.WINDOW_HEIGHT * 0.555:
                print("按下「新遊戲」")
                self.menuButtonPos = (0, 0)

            if mouse_y > self.WINDOW_HEIGHT * 0.605 and mouse_y < self.WINDOW_HEIGHT * 0.74:

                # 選項
                if mouse_x < self.WINDOW_WIDTH * 0.375:
                    print("按下「選項」")
                    self.menuButtonPos = (0, 0)

                # 說明
                if mouse_x > self.WINDOW_WIDTH * 0.525:
                    print("按下「說明」")
                    self.menuButtonPos = (0, 0)

        pygame.display.flip()

    def renderplay(self):
        """
        Render the game play.
        """
        self.refresh()

    def renderhelp(self):
        """
        Render the help screen.
        """

        self.screen.fill(BACKGROUND_BLUE)
        somewords = self.smallfont.render(
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
        self.screen.fill(BACKGROUND_BLUE)

        self.screen.blit(self.background_image, (0, 0))

        somewords = self.smallfont.render('You are Playing the game. F1 for help.', True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        self.creatures.update()
        self.creatures.draw(self.screen)
        self.straws.update()
        self.straws.draw(self.screen)
        self.hearts.update()
        self.hearts.draw(self.screen)
        
        # score counter
        self.turtleCounter += 1
        score = self.smallfont.render(str(self.turtleCounter // 6), False, (0, 0, 0))
        score_rect = score.get_rect(topright = (self.WINDOW_WIDTH , 0))
        self.screen.blit(score, score_rect)
        
        # 碰撞
        pygame.draw.rect(self.screen, (255, 0, 0), self.creature.hitBox, 2)
        # print(pygame.sprite.spritecollideany(self.creature, self.straws, pygame.sprite.collide_rect))

        pygame.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        if not os.path.isfile('config.ini'):
            resolutionWidth = 1280
            resolutionHeight = 720
            screenFlags = pygame.SCALED
            display_index = 0
            vsync = 1
            self.generateConfig()
        else:
            resolutionWidth, resolutionHeight, screenFlags, display_index, vsync = self.applyConfig()

        result = pygame.init()
        pygame.init()
        pygame.font.init()
        #pygame.display.init()
        pygame.display.set_caption('Green Sea Turtle Adventure')
        self.screen = pygame.display.set_mode((resolutionWidth, resolutionHeight),
                                                screenFlags,
                                                display = display_index,
                                                vsync = vsync)
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font("src/jf-openhuninn-1.1.ttf", 40)
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
