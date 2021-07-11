import pygame
from src.event_manager import *

class GameEngine(object):
    """
    Tracks the game state.
    """

    def __init__(self, event_manager):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False
        self.state = StateMachine()

    def notify(self, event):
        """
        Called by an event in the message queue.
        """

        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.event_manager.post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.event_manager.post(InitializeEvent())
        self.state.push(STATE_INTRO)
        while self.running:
            new_tick = TickEvent()
            self.event_manager.post(new_tick)

# State machine constants for the StateMachine class below
STATE_INTRO = 1
STATE_MENU = 2
STATE_HELP = 3
STATE_OPTIONS  = 4
STATE_PLAY = 5
STATE_DIED = 6

class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """

    def __init__ (self):
        self.state_stack = []

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.state_stack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.state_stack.pop()
            return len(self.state_stack) > 0
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.state_stack.append(state)
        return state
