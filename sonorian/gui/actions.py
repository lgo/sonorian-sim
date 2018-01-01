

class ActionMap(dict):
    """
    Map of action to event handler.

    TODO(joey): Does this need to be specialized? I suspect it may, so
    this will remain used.
    """
    pass


class Action(object):
    """
    Represents a user action, often associated with event handlers.
    """

    def __init__(self, key, name, fn):
        self.key = key
        self.name = name
        self.fn = fn


#: Actions available on the home screen.
ACTIONS_HOMESCREEN = [
    Action('g', 'generate'),
    Action('q', 'quit'),
]
