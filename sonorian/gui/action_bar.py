import curses

from sonorian.gui.status import STATUS_OK, STATUS_ERROR
# FIXME(joey): Circular import. This is only needed for type-checking tbh.
#from .actions import Action


ACTION_BAR_HEIGHT = 3


class ActionBar(object):
    """
    Interface bar displaying the available actions and previous action
    status.
    """

    class State(object):
        """
        Represents mutable state of the action bar. Modifying State
        values corresponds to display changes.
        """
        # TODO(joey): This is a weird attempt at dividing the
        # serializable state from the working state. We shall see how
        # this goes.
        def __init__(self):
            self.available_actions = [] # type: ListOf[actions.Action]
            self.msg = None # type: str
            self.status = None # type: int

    def __init__(self, stdscr):
        self.parent_scr = stdscr
        self.parent_height, self.parent_width = self.parent_scr.getmaxyx()
        self.scr = self.parent_scr.subwin(
            self.parent_height - ACTION_BAR_HEIGHT, 0)
        self.state = ActionBar.State()

    def set_actions(self, actions, refresh=True):
        """
        Sets the available actions and updates the display.
        """
        # TODO(joey): Set up the ActionMap and event handling.
        self.state.available_actions = actions
        self._redraw_actions()
        if refresh:
            self.scr.refresh()

    def set_msg(self, msg, status=STATUS_OK, refresh=True):
        """
        Set msg displayed in the action bar. By default the screen will
        be refreshed.
        """
        self.state.msg = msg
        self.state.status = status
        self.scr.addstr(
            2, 2, msg, curses.color_pair(status))
        self.scr.clrtoeol()

        if refresh:
            self.scr.refresh()

    def resize(self):
        """
        Resize the action bar.
        """
        (height, width) = self.parent_scr.getmaxyx()
        needsRefresh = False

        # Resize and redraw the action bar if the width changes and move
        # the action bar if the height changes.
        if self.parent_width != width:
            self.scr.resize(ACTION_BAR_HEIGHT, width)
            self.redraw()
            needsRefresh = True
        if self.parent_height != height:
            self.scr.mvwin(height - ACTION_BAR_HEIGHT, 0)
            needsRefresh = True

        if needsRefresh:
            self.scr.refresh()

        self.parent_height, self.parent_width = height, width

    def redraw(self):
        """
        Redraw the action bar.
        """
        self.scr.border(
            ' ', ' ', 0, ' ', curses.ACS_HLINE, curses.ACS_HLINE, ' ', ' ')
        self._redraw_actions()
        self.scr.addstr(2, 0, '>')

    def _redraw_actions(self):
        action_strs = ["({key}) {name}".format(key=action.key(), name=action.name)
                       for action in self.state.available_actions]
        self.scr.addstr(1, 0, "   ".join(action_strs))
        self.scr.clrtoeol()

