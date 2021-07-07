import pygame
import model
from eventmanager import *

class Keyboard(object):
    """
    Handles keyboard input.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():

                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.evManager.Post(QuitEvent())

                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.evManager.Post(StateChangeEvent(None))
                    else:
                        currentstate = self.model.state.peek()
                        if currentstate == model.STATE_INTRO:
                            self.keydownintro(event)
                        if currentstate == model.STATE_MENU:
                            self.keydownmenu(event)
                        if currentstate == model.STATE_HELP:
                            self.keydownhelp(event)
                        if currentstate == model.STATE_PLAY:
                            self.keydownplay(event)
                        #設定尚未放開方向鍵就改變方向
                        if currentstate == model.STATE_RIGHT or currentstate == model.STATE_LEFT or currentstate == model.STATE_UP or currentstate == model.STATE_DOWN:
                            self.keyupPlay()
                            self.keydownplay(event)

                # handle key up events
                if event.type == pygame.KEYUP:
                    currentstate = self.model.state.peek()
                    if currentstate == model.STATE_RIGHT and event.key == pygame.K_RIGHT:
                        self.keyupPlay()
                    if currentstate == model.STATE_LEFT and event.key == pygame.K_LEFT:
                        self.keyupPlay()
                    if currentstate == model.STATE_UP and event.key == pygame.K_UP:
                        self.keyupPlay()
                    if currentstate == model.STATE_DOWN and event.key == pygame.K_DOWN:
                        self.keyupPlay()

    def keydownintro(self, event):
        """
        Handles intro key events.
        """
        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        if event.key == pygame.K_SPACE:
            self.evManager.Post(StateChangeEvent(model.STATE_MENU))

    def keydownmenu(self, event):
        """
        Handles menu key events.
        """

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        # space plays the game
        if event.key == pygame.K_SPACE:
            self.evManager.Post(StateChangeEvent(model.STATE_PLAY))
        if event.key == pygame.MOUSEBUTTONUP:
            print("pygame.MOUSEBUTTONUP is working")
            self.evManager.Post(InputEvent(None, event.pos))

    def keydownhelp(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.evManager.Post(StateChangeEvent(None))

    def keydownplay(self, event):
        """
        Handles play key events.
        """
        # ESC back to menu
        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        else:
            self.evManager.Post(InputEvent(event.unicode, None))

        # F1 shows the help
        if event.key == pygame.K_F1:
            self.evManager.Post(StateChangeEvent(model.STATE_HELP))

        # Arrow keys to control character
        if event.key == pygame.K_RIGHT:
            self.evManager.Post(StateChangeEvent(model.STATE_RIGHT))
        if event.key == pygame.K_LEFT:
            self.evManager.Post(StateChangeEvent(model.STATE_LEFT))
        if event.key == pygame.K_UP:
            self.evManager.Post(StateChangeEvent(model.STATE_UP))
        if event.key == pygame.K_DOWN:
            self.evManager.Post(StateChangeEvent(model.STATE_DOWN))

    def keyupPlay(self):
        """
        放開按鍵回到play重新判斷有沒有按任一方向鍵
        """
        self.evManager.Post(StateChangeEvent(None))
