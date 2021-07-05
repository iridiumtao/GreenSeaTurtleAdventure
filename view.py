import pygame
import model
from eventmanager import *
import configparser
import os.path

BACKGROUND_BLUE = (93, 189, 245)
#screenFlags = pygame.FULLSCREEN | pygame.SCALED
screenFlags = pygame.SCALED

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

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_MENU:
                self.rendermenu()
            if currentstate == model.STATE_PLAY:
                self.renderplay()
            if currentstate == model.STATE_HELP:
                self.renderhelp()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

    def rendermenu(self):
        """
        Render the game menu.
        """

        """
        todo:
        1.

        """
        self.screen.fill(BACKGROUND_BLUE)
        white = (255, 255, 255)
        select = []

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

        pygame.display.flip()

    def renderplay(self):
        """
        Render the game play.
        """

        self.screen.fill(BACKGROUND_BLUE)
        somewords = self.smallfont.render(
                    'You are Playing the game. F1 for help.',
                    True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()

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

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        # file = open("basic_setting.txt", encoding="utf-8")
        # lines = fp.readline()
        #
        # while lines:
        #     line = fp.readline()

        if not os.path.isfile('config.ini'):
            self.config()

        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Green Sea Turtle Adventure')
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font("src/jf-openhuninn-1.1.ttf", 40)
        self.isinitialized = True

    def config(self):
        config = configparser.ConfigParser()
        config['SCREEN'] = {'RESOLUTION_WIDTH' : '1920',
                            'RESOLUTION_HEIGHT' : '1080',
                            'FULLSCREEN' : 'TRUE',
                            'SCALED' : 'FALSE',
                            'NOFRAME' : 'FALSE'}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
