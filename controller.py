import pygame
import model
from eventmanager import *

class Keyboard(object):
    """
    Handles keyboard input.
    """

    def __init__(self, event_manager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.event_manager = event_manager
        event_manager.RegisterListener(self)
        self.model = model
        self.lastKey = None

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():

                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.event_manager.Post(QuitEvent())

                currentstate = self.model.state.peek()

                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.Post(StateChangeEvent(None))
                    else:
                        if currentstate == model.STATE_INTRO:
                            self.keyDownIntro(event)
                        if currentstate == model.STATE_MENU:
                            self.keyDownMenu(event)
                        if currentstate == model.STATE_HELP:
                            self.keyDownHelp(event)
                        if currentstate == model.STATE_PLAY:
                            self.keyDownPlay(event)
                        #設定尚未放開方向鍵就改變方向

                # handle key up events
                if event.type == pygame.KEYUP:
                    if currentstate == model.STATE_PLAY:
                        self.keyUpPlay(event)

                if event.type == pygame.MOUSEBUTTONUP:
                    if currentstate == model.STATE_MENU:
                        self.mouseButtonUpMenu(event)


    def keyDownIntro(self, event):
        """
        Handles intro key events.
        """
        if event.key == pygame.K_ESCAPE:
            self.event_manager.Post(StateChangeEvent(None))
        if event.key == pygame.K_SPACE:
            self.event_manager.Post(StateChangeEvent(model.STATE_MENU))

    def keyDownMenu(self, event):
        """
        Handles menu key events.
        """

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.event_manager.Post(StateChangeEvent(None))

    def keyDownHelp(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.event_manager.Post(StateChangeEvent(None))

    def keyDownOptions(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.event_manager.Post(StateChangeEvent(None))

    def keyDownPlay(self, event):
        """
        Handles play key events.
        """
        # ESC back to menu
        if event.key == pygame.K_ESCAPE:
            self.event_manager.Post(StateChangeEvent(None))
        else:
            self.lastKey = event.key
            self.event_manager.Post(InputEvent(event.key, None))

        # F1 shows the help
        if event.key == pygame.K_F1:
            self.event_manager.Post(StateChangeEvent(model.STATE_HELP))

    def keyUpPlay(self, event):
        """
        放開按鍵
        """
        if self.lastKey == event.key:
            self.event_manager.Post(InputEvent(None, None))

    def mouseButtonUpMenu(self, event):
        # MENU 按下去之後傳送滑鼠位置
        self.event_manager.Post(InputEvent(None, event.pos))
