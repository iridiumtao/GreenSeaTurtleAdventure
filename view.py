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


BACKGROUND_COLOR = (93, 189, 245)
DEFAULT_COLOR = (255, 255, 255)

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, event_manager, model):
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
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.small_font = None

        self.turtle_score = 0
        self.turtle_heart = 2
        self.intro_text_alpha = 255

        self.menu_button_pos = (0, 0)
        self.temp_num = 0
        self.menu_button_state = 0

        self.key = 0
        self.first_time = True
        self.turtle_died = False


    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, InitializeEvent):
            self.initialize()

            self.background_image = pygame.image.load("src/background.png").convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))

            self.help_background_image = pygame.image.load("src/help-inside.jpg").convert_alpha()
            self.help_background_image = pygame.transform.scale(self.help_background_image, (self.window_width, self.window_height))


            # add intro page objects
            self.bigTurtle = IntroObject.IntroObject(self.window_width, self.window_height, w=858, h=672, x=-1000, y=150, stopX=-400, rate=8, turn=-15)
            self.bigStraw1 = IntroObject.IntroObject(self.window_width, self.window_height, w=200, h=700, x=1100, y=390, stopX=900, rate=-8, turn=-60, flip=True, image="src/straw.png")
            self.bigStraw2 = IntroObject.IntroObject(self.window_width, self.window_height, w=200, h=700, x=1100, y=350, stopX=950, rate=-8, turn=-50, flip=True, image="src/straw.png")
            self.bigStraw3 = IntroObject.IntroObject(self.window_width, self.window_height, w=200, h=700, x=1100, y=300, stopX=900, rate=-8, turn=-40, flip=True, image="src/straw.png")

            # 生成 menu 按鈕
            self.menuContinueButton = MenuButton.MenuButton(x = self.window_width * 0.34,
                                                            y = self.window_height * 0.235,
                                                            w = self.window_width * 0.32,
                                                            h = self.window_height * 0.135,
                                                            image = "src/continue-button.png")
            self.menu_new_game_button = MenuButton.MenuButton(x = self.window_width * 0.34,
                                                           y = self.window_height * 0.42,
                                                           w = self.window_width * 0.32,
                                                           h = self.window_height * 0.135,
                                                           image = "src/start-button.png")
            self.menu_option_button = MenuButton.MenuButton(x = self.window_width * 0.34,
                                                          y = self.window_height * 0.605,
                                                          w = self.window_width * 0.135,
                                                          h = self.window_height * 0.135,
                                                          image = "src/option-button.png")
            self.menu_help_button = MenuButton.MenuButton(x = self.window_width * 0.525,
                                                        y = self.window_height * 0.605,
                                                        w = self.window_width * 0.135,
                                                        h = self.window_height * 0.135,
                                                        image = "src/help-button.png")

            self.menuBigContinueButton = MenuButton.MenuButton(x = self.window_width * 0.32,
                                                            y = self.window_height * 0.225,
                                                            w = self.window_width * 0.36,
                                                            h = self.window_height * 0.155,
                                                            image = "src/continue-button.png")
            self.menuBigGameButton = MenuButton.MenuButton(x = self.window_width * 0.32,
                                                           y = self.window_height * 0.41,
                                                           w = self.window_width * 0.36,
                                                           h = self.window_height * 0.155,
                                                           image = "src/start-button.png")
            self.menuBigOptionButton = MenuButton.MenuButton(x = self.window_width * 0.33,
                                                          y = self.window_height * 0.600,
                                                          w = self.window_width * 0.155,
                                                          h = self.window_height * 0.145,
                                                          image = "src/option-button.png")
            self.menu_big_help_button = MenuButton.MenuButton(x = self.window_width * 0.515,
                                                        y = self.window_height * 0.600,
                                                        w = self.window_width * 0.155,
                                                        h = self.window_height * 0.145,
                                                        image = "src/help-button.png")

            self.menu_buttons = pygame.sprite.Group((self.menuContinueButton,) +
                                                   (self.menu_new_game_button,) +
                                                   (self.menu_option_button,) +
                                                   (self.menu_help_button,))


            # 生成海龜
            self.creatures = pygame.sprite.Group()
            self.creature = TurtleMC.TurtleMC(1/5, self.window_width, self.window_height)
            self.creatures.add(self.creature)

            # 生成吸管
            self.straws = pygame.sprite.Group()
            strawNum = 10
            for i in range(strawNum):
                # self.straws.add(Straw.Straw(self.WINDOW_WIDTH, random.randint(self.WINDOW_WIDTH, self.WINDOW_WIDTH*2), (self.WINDOW_HEIGHT/strawNum)*i+10))
                self.straws.add(Straw.Straw(self.window_width, self.window_height))

            self.spawnTurtleHeart(self.turtle_heart)

        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
             # Called for each game tick. We check our keyboard presses here.
            if not self.isinitialized:
                return
            # 切換頁面
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_INTRO:
                self.renderIntro()
            if currentstate == model.STATE_MENU:
                self.renderMenu(event)
            if currentstate == model.STATE_PLAY:
                self.renderPlay()
            if currentstate == model.STATE_HELP:
                self.renderHelp()
            if currentstate == model.STATE_OPTIONS:
                self.renderOptions()

            # 設定 60 FPS
            self.clock.tick(60)

        elif isinstance(event, InputEvent):
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_MENU:
                self.menu_button_pos = event.click_pos
            if currentstate == model.STATE_PLAY:
                self.key = event.key

    def renderIntro(self):
        self.screen.fill(DEFAULT_COLOR)
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background_image, (0, 0))

        text = self.small_font.render(
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
        text_rect = text.get_rect(center = (self.window_width / 2, self.window_height * 0.8))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def renderMenu(self, event):
        """
        Render the game menu.
        """

        self.screen.fill(BACKGROUND_COLOR)

        self.screen.blit(self.background_image, (0, 0))




        mouse_focused_sprite = pygame.sprite.Group()

        # 繼續遊戲按鈕的顯示與否
        if self.first_time or self.turtle_died:
            self.menu_buttons.remove(self.menuContinueButton)
        else:
            self.menu_buttons.add(self.menuContinueButton)
            # 繼續遊戲
            if self.menuContinueButton.rect.collidepoint(self.menu_button_pos):
                print("按下「繼續遊戲」")
                self.event_manager.post(StateChangeEvent(model.STATE_PLAY))
                self.menu_button_pos = (0, 0)

            if self.menuContinueButton.rect.collidepoint(pygame.mouse.get_pos()):
                mouse_focused_sprite = pygame.sprite.Group((self.menuBigContinueButton,))

        # 新遊戲
        if self.menu_new_game_button.rect.collidepoint(self.menu_button_pos):
            print("按下「新遊戲」")
            self.setTurtleState(TurtleMC.TURTLE_ALIVE)
            self.turtle_score = 1
            self.spawnTurtleHeart(2)
            self.event_manager.post(StateChangeEvent(model.STATE_PLAY))
            self.menu_button_pos = (0, 0)

        if self.menu_new_game_button.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_focused_sprite = pygame.sprite.Group((self.menuBigGameButton,))

        # 選項
        if self.menu_option_button.rect.collidepoint(self.menu_button_pos):
            print("按下「選項」")
            self.event_manager.post(StateChangeEvent(model.STATE_OPTIONS))
            self.menu_button_pos = (0, 0)

        if self.menu_option_button.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_focused_sprite = pygame.sprite.Group((self.menuBigOptionButton,))

        # 說明
        if self.menu_help_button.rect.collidepoint(self.menu_button_pos):
            print("按下「說明」")
            self.event_manager.post(StateChangeEvent(model.STATE_HELP))
            self.menu_button_pos = (0, 0)

        if self.menu_help_button.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_focused_sprite = pygame.sprite.Group((self.menu_big_help_button,))

        self.menu_buttons.draw(self.screen)

        for button in self.menu_buttons:
            button.update()

        mouse_focused_sprite.update()
        mouse_focused_sprite.draw(self.screen)

        pygame.display.flip()

    def renderOptions(self):
        """
        Render the options screen.
        """

        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background_image, (0, 0))

        somewords = self.small_font.render(
                    'Options is here. space, escape or return.',
                    True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()

    def renderHelp(self):
        """
        Render the help screen.
        """

        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.help_background_image, (0, 0))

        pygame.display.flip()

    def renderPlay(self):
        """
        Render the game play.
        """

        self.first_time = False

        if not self.turtle_died:
            if self.key == pygame.K_RIGHT:
                self.creature.move("right")
            if self.key == pygame.K_LEFT:
                self.creature.move("left")
            if self.key == pygame.K_UP:
                self.creature.move("up")
            if self.key == pygame.K_DOWN:
                self.creature.move("down")

        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background_image, (0, 0))

        somewords = self.small_font.render('You are Playing the game. F1 for help.', True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        self.creatures.update()
        self.creatures.draw(self.screen)
        self.straws.update()
        self.straws.draw(self.screen)
        self.hearts.update()
        self.hearts.draw(self.screen)

        # score counter
        if not self.turtle_died:
            self.turtle_score += 1
        score = self.small_font.render(str(self.turtle_score // 6), False, (0, 0, 0))
        score_rect = score.get_rect(topright = (self.window_width , 0))
        self.screen.blit(score, score_rect)

        # 顯示hitBox
        pygame.draw.rect(self.screen, (255, 0, 0), self.creature.hit_box.rect, 2)

        # hitbox觸發
        strawsDamage = pygame.sprite.spritecollide(self.creature.hit_box, self.straws, False)
        if(strawsDamage):
            self.strawsDamage(strawsDamage)

        pygame.display.flip()

    def spawnTurtleHeart(self, heartNum):
        # 生成心臟
        self.hearts = pygame.sprite.Group()
        # heartSize = 52
        for i in range(heartNum):
            # self.hearts.add(Heart.Heart(0 + i * heartSize, self.windowHeight - heartSize, heartSize))
            self.hearts.add(Heart.Heart(i, self.window_width, self.window_height))

    def strawsDamage(self, strawsDamage):

        for straw in strawsDamage:
            self.straws.remove(straw)
            self.straws.add(Straw.Straw(self.window_width, self.window_height))

        currentHearts = len(self.hearts)
        if currentHearts == 0:
            print("game over")
            self.setTurtleState(TurtleMC.TURTLE_DIED)
            pass
             #gameover
            return

        if currentHearts <= self.turtle_heart // 2:
            self.setTurtleState(TurtleMC.TURTLE_DYING)

        self.hearts.remove(self.hearts.sprites()[currentHearts - 1])


    def setTurtleState(self, state):
        if state == TurtleMC.TURTLE_ALIVE:
            self.creature.setImageSetNum(TurtleMC.TURTLE_ALIVE)
            self.turtle_died = False
        elif state == TurtleMC.TURTLE_DYING:
            self.creature.setImageSetNum(TurtleMC.TURTLE_DYING)
            self.turtle_died = False
        elif state == TurtleMC.TURTLE_DIED:
            self.creature.setImageSetNum(TurtleMC.TURTLE_DIED)
            self.turtle_died = True


    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        if not os.path.isfile('config.ini'):
            resolution_width = 1280
            resolution_height = 720
            screen_flags = pygame.SCALED
            display_index = 0
            vsync = 1
            self.generate_config()
        else:
            resolution_width, resolution_height, screen_flags, display_index, vsync = self.apply_config()

        result = pygame.init()
        pygame.init()
        pygame.font.init()
        #pygame.display.init()
        pygame.display.set_caption('Green Sea Turtle Adventure')
        self.screen = pygame.display.set_mode((resolution_width, resolution_height),
                                                screen_flags,
                                                display = display_index,
                                                vsync = vsync)
        self.window_width, self.window_height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font("src/jf-openhuninn-1.1.ttf", 40)
        self.isinitialized = True

    def generate_config(self):
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

        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    def apply_config(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')

            screen = config['SCREEN']

            resolution_width = int(screen['resolution_width'])
            resolution_height = int(screen['resolution_height'])
            screen_flags = 0
            if screen.getboolean('fullscreen'):
                screen_flags = pygame.FULLSCREEN
            if screen.getboolean('scaled'):
                screen_flags = screen_flags | pygame.SCALED
            if screen.getboolean('noframe'):
                screen_flags = screen_flags | pygame.NOFRAME
            if screen.getboolean('opengl'):
                screen_flags = screen_flags | pygame.OPENGL
            display_index = int(screen['display_index'])
            vsync = int(screen['vsync'])
            return resolution_width, resolution_height, screen_flags, display_index, vsync
        except:
            self.generate_config()
            return 1280, 720, pygame.SCALED, 0, 1
