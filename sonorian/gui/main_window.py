import sys
import curses
from .action_bar import ActionBar, STATUS_OK, STATUS_ERROR
from .actions import ActionMap, ACTIONS_HOMESCREEN

class MainWindow(object):
    """
    Provides an interactive interface for World using ncurses.
    """

    def __init__(self):
        self.world = None
        self.action_map = ActionMap()
        pass

    def loop(self):
        """
        Begin the interactive window.
        """
        try:
            curses.wrapper(self._loop)
        except (SystemExit, KeyboardInterrupt):
            pass

    def _loop(self, stdscr):
        """
        Internal interactive loop. It is executed using curses.wrapper
        to recover terminal settings after execution.
        """
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()

        # Hide the cursor.
        curses.curs_set(0)

        # Initialize colours.
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        # Initialize the action bar.
        self.action_bar = ActionBar(self.stdscr)
        self.set_actions(ACTIONS_HOMESCREEN)
        self.action_bar.redraw()

        # Start receiving input.
        while True:
            self._input_loop()

    def _input_loop(self):
        """
        Receive input and execute an action.
        """
        ch = self.stdscr.getch()
        if ch == curses.KEY_RESIZE:
            self.call_for_resize()
        elif ch == -1:
            # No input is available. no-op
            pass
        elif ch in self.action_map:
            self.action_map[ch].run_action(self)
        elif ch == ord('g'):
            self.action_bar.set_msg(
                '(would have) generated world', status=STATUS_OK)
        else:
            msg = None
            # ch is not always a valid character. For example, negative
            # error codes may be returned.
            if 0 < ch and ch < 0x110000:
                msg = 'invalid key (%d/%c)' % (ch, ch)
            else:
                msg = 'invalid key (%d)' % ch
            self.action_bar.set_msg(msg, status=STATUS_ERROR)

    def call_for_resize(self):
        """
        Called when we want to resize the screen.
        """
        (height, width) = self.stdscr.getmaxyx()
        self.redraw_world()
        self.action_bar.resize()
        self.height, self.width = height, width

    def redraw_world(self):
        self.stdscr.clear()

    def set_actions(self, actions):
        """
        Sets the available user actions. This involves:
        1) Updating the action bar display.
        2) Updating the action map for event handling.
        """
        self.action_bar.set_actions(actions)
        self.action_map.clear()
        for action in actions:
            self.action_map[action.key] = action

