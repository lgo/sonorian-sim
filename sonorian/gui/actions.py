import collections
import sys
# from .action_bar import STATUS_OK


class MenuTree(collections.OrderedDict):
    """
    Map of action to event handler.
    """
    # FIXME(joey): Raise a SyntaxError if the key already exists.

    @staticmethod
    def get_path(tree, path):
        """
        Fetches the menu item, given a path.

        Returns:
            A MenuTree or an Action.
        """
        # FIXME(joey): Come up with a better path delimiter.
        parts = path.split('|')
        for part in parts:
            if part not in tree:
                return None
            tree = tree[part]
        return tree

    def __str__(self, level=0):
        item_strs = []
        for item in self.values():
            item_strs.append(item.__str__(level + 1))
        return "\n".join(item_strs)

class Submenu(MenuTree):

    # FIXME(joey): Raise a SyntaxError if inserting b, which is
    # typically 'back'.

    def __init__(self, key, name):
        # FIXME(joey): Is this correct?
        super()
        self.key = key
        self.name = name

    def __str__(self, level=0):
        submenu_line = ("  " * level) + \
            "({key}) {name}".format(key=self.key, name=self.name)
        submenu_back_line = ("  " * (level+1)) + "(b) back"
        item_strs = [submenu_line]
        for item in self.values():
            item_strs.append(item.__str__(level + 1))
        item_strs.append(submenu_back_line)
        return "\n".join(item_strs)

class Action(object):
    """
    Represents a user action, often associated with event handlers.
    """

    def __init__(self, key, name, fn):
        self.key = key
        self.name = name
        self.fn = fn

    def __str__(self, level=0):
        return ("  " * level) + "({key}) {name}".format(key=self.key, name=self.name)

class MenuTreeGenerator(object):
    """
    DSL for generating a menu-tree of actions in the form of an
    MenuTree.

    For an example of the DSL:

        g = MenuTreeGenerator()
        g += Action('g', 'generate', ...)
        with g.submenu('s', 'settings'):
            g += Action('p', 'probability', ...)
    """
    # TODO(joey): Add conditionals for displaying / enabling actions.

    def __init__(self):
        self._active_menu = MenuTree()
        self._next_submenu = None
        self._menu_stack = []

    def submenu(self, key, name):
        """
        Initializes a sub-menu to be used. This function should only be
        called using 'with', for example:

            g = MenuTreeGenerator()
            with g.submenu('s', 'settings'):
                g += Action('n', 'name', ...)

        """
        if self._next_submenu is not None:
            raise SyntaxError("cannot call submenu without using 'with' keyword")
        self._next_submenu = Submenu(key, name)
        return self

    def __enter__(self):
        """
        Enter the sub-menu context. The sub-menu must have been set up
        using submenu().
        """
        if self._next_submenu is None:
            raise SyntaxError(
                "cannot use 'with' keyword without calling submenu")
        # In order to manage the context:
        # 1) The current menu item is pushed to the menu_stack.
        # 3) The previously initialized sub-menu is made active.
        self._menu_stack.append(self._active_menu)
        self._active_menu = self._next_submenu
        self._next_submenu = None

    def __exit__(self, exc_type, exc_value, traceback):
        # FIXME(joey): Handle exceptions correctly.
        if self._next_submenu is not None:
            raise SyntaxError(
                "invalid usage")

        current_menu = self._active_menu
        # Recover the last menu.
        self._active_menu = self._menu_stack.pop()
        # Append the current to its parent menu.
        self._active_menu[current_menu.key] = current_menu


    def __iadd__(self, action):
        """
        DSL concatenation of an action.
        """
        self._active_menu[action.key] = action
        return self

    def finish(self):
        if len(self._menu_stack) > 0:
            raise SyntaxError("called finish() before exiting all sub-menus")
        if self._next_submenu is not None:
            raise SyntaxError("called finish() after calling submenu()")
        return self._active_menu

def _generate(window):
    pass
    # FIXME(joey): Import issues while testing this. Ideally, this is a
    # rather independant package, except for the menu population itself.
    # self.action_bar.set_msg( '(would have) generated world',
    # status=STATUS_OK)

def _quit(window):
    sys.exit(0)

def _settings_size(window):
    pass


def _settings_probability(window):
    pass

def populate_menu(actions):
    actions += Action('g', 'generate', _generate)

    with g.submenu('s', 'settings'):
        actions += Action('s', 'size', _settings_size)
        actions += Action('p', 'probability', _settings_probability)

    actions += Action('q', 'quit', _quit)

    return actions.finish()

if __name__ == "__main__":
    g = MenuTreeGenerator()
    menu = populate_menu(g)
    print("==== MENU TREE ====")
    print(menu)
