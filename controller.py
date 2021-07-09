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
        event_manager.register_listener(self)
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
                    self.event_manager.post(QuitEvent())

                currentstate = self.model.state.peek()

                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.post(StateChangeEvent(None))
                    else:
                        if currentstate == model.STATE_INTRO:
                            self.key_down_intro(event)
                        if currentstate == model.STATE_MENU:
                            self.key_down_menu(event)
                        if currentstate == model.STATE_HELP:
                            self.key_down_help(event)
                        if currentstate == model.STATE_PLAY:
                            self.key_down_play(event)
                        #設定尚未放開方向鍵就改變方向

                # handle key up events
                if event.type == pygame.KEYUP:
                    if currentstate == model.STATE_PLAY:
                        self.key_up_play(event)

                if event.type == pygame.MOUSEBUTTONUP:
                    if currentstate == model.STATE_MENU:
                        self.mouse_button_up_menu(event)


    def key_down_intro(self, event):
        """
        Handles intro key events.
        """
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))
        if event.key == pygame.K_SPACE:
            self.event_manager.post(StateChangeEvent(model.STATE_MENU))

    def key_down_menu(self, event):
        """
        Handles menu key events.
        """

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))

    def key_down_help(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.event_manager.post(StateChangeEvent(None))

    def key_down_options(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.event_manager.post(StateChangeEvent(None))

    def key_down_play(self, event):
        """
        Handles play key events.
        """
        # ESC back to menu
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))
        else:
            self.lastKey = event.key
            self.event_manager.post(InputEvent(event.key, None))

        # F1 shows the help
        if event.key == pygame.K_F1:
            self.event_manager.post(StateChangeEvent(model.STATE_HELP))

    def key_up_play(self, event):
        """
        放開按鍵
        """
        if self.lastKey == event.key:
            self.event_manager.post(InputEvent(None, None))

    def mouse_button_up_menu(self, event):
        # MENU 按下去之後傳送滑鼠位置
        self.event_manager.post(InputEvent(None, event.pos))
