"""
menu_builder provides a DSL and interfaces for creating a MenuTree. A
MenuTree is composed of MenuItems, which are either Submenu sub-trees or
Actions leaf nodes.
"""

from abc import ABC, abstractmethod
import collections
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class MenuItem(ABC):
    """
    An interface that must be implemented for all
    items that are inserted into the MenuTree.
    """

    @abstractmethod
    def key(self):
        """
        The key uniquely identifying the MenuItem.
        """
        raise NotImplementedError()

    @abstractmethod
    def fn(self):
        """
        Return the action to execute on MenuItem selection.
        """
        raise NotImplementedError()


class MenuTree(collections.OrderedDict):
    """
    TODO(joey): Document.
    """

    def __init__(self):
        self.data = {}

    def add(self, item):
        """
        Add a MenuItem to the MenuTree.
        """
        if not isinstance(item, MenuItem):
            raise NotImplementedError("{classname} does not implement MenuItem interface".format(
                classname=typeof(classname)))
        if item.key() in self.data:
            raise SyntaxError("bad MenuTree: item={item} already exists in map".format(item=item))
        self.data[item.key()] = item

    def get_path(self, path):
        """
        Fetches the menu item, given a path.

        Returns:
            A MenuTree or an Action.
        """
        tree = self
        # TODO(joey): Come up with a better path delimiter. Even better,
        # change the input a list of keys.
        parts = path.split('|')
        for part in parts:
            if part not in tree:
                return None
            tree = tree[part]
        return tree

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None

    def __iter__(self):
        return iter(self.data.values())

    def __str__(self, level=0):
        item_strs = []
        for item in self.data.values():
            item_strs.append(item.__str__(level + 1))
        return "\n".join(item_strs)

    def __in__(self, item):
        return item in self.data

class Submenu(MenuTree, MenuItem):
    """
    TODO(joey): Document.
    """

    def __init__(self, key, name):
        super().__init__()
        self._key = key
        self.name = name

    def key(self):
        """
        key implements the MenuItem interface.
        """
        return self._key

    def fn(self):
        """
        fn implements the MenuItem interface.
        """
        # TODO(joey): Maybe the fn call for Submenu should be owned
        # completely by window to happen. The location of this fcn is
        # obscure.
        return lambda window: window.menu_enter(self.key)

    def __str__(self, level=0):
        submenu_line = ("  " * level) + \
            "({key}) {name}".format(key=self.key(), name=self.name)
        item_strs = [submenu_line]
        for item in self.data.values():
            item_strs.append(item.__str__(level + 1))
        return "\n".join(item_strs)

    def __repr__(self):
        return "<Submenu key={key} name={name}>".format(key=self.key(), name=self.name)


class Action(MenuItem):
    """
    Represents a user action, often associated with event handlers.
    """

    def __init__(self, key, name, fn):
        self._key = key
        self.name = name
        self._fn = fn

    def key(self):
        """
        key implements the MenuItem interface.
        """
        return self._key

    def fn(self):
        """
        fn implements the MenuItem interface.
        """
        return self._fn

    def __str__(self, level=0):
        return ("  " * level) + "({key}) {name}".format(key=self.key(), name=self.name)

    def __repr__(self):
        return "<Action key={key} name={name}>".format(key=self.key(), name=self.name)


def _submenu_back(window):
    """
    _back is an action for moving back from a sub-menu.
    """
    # TODO(joey): Maybe this fcn can be moved, its location is a bit
    # obscure.
    window.menu_back()


SUBMENU_BACK_ACTION = Action('b', 'back', _submenu_back)


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
    # TODO(joey): Add conditionals for displaying or enabling actions.
    # This could possibly be done by adding a fn parameter to the
    # constructor of MenuItems that can be evaluated when loading the
    # menu.

    def __init__(self):
        self._active_menu = MenuTree()
        self._next_submenu = None
        self._menu_stack = []

    def submenu(self, key, name):
        """
        Initializes a sub-menu to be used. This function should only be
        called using 'with'.
        """
        if self._next_submenu is not None:
            raise SyntaxError(
                "cannot call submenu without using 'with' keyword")
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
        # TODO(joey): Handle exceptions correctly.
        if self._next_submenu is not None:
            raise SyntaxError(
                "invalid usage")

        current_menu = self._active_menu
        # Add a 'back' action to each sub-menu.
        current_menu.add(SUBMENU_BACK_ACTION)
        # Recover the last menu.
        self._active_menu = self._menu_stack.pop()
        # Append the current to its parent menu.
        self._active_menu.add(current_menu)

    def __iadd__(self, action):
        """
        DSL operator for adding an Action to the menu.
        """
        self._active_menu.add(action)
        return self

    def finish(self):
        """
        Produce the complete menu tree.
        """
        if len(self._menu_stack) > 0:
            raise SyntaxError("called finish() before exiting all sub-menus")
        if self._next_submenu is not None:
            raise SyntaxError("called finish() after calling submenu()")
        return self._active_menu


if __name__ == "__main__":
    def test_populate_menu(actions):
        actions += Action('g', 'generate', None)
        with g.submenu('s', 'settings'):
            actions += Action('s', 'size', None)
            actions += Action('p', 'probability', None)
        actions += Action('q', 'quit', None)
        return actions.finish()

    g = MenuTreeGenerator()
    menu = test_populate_menu(g)
    print("==== MENU TREE ====")
    print(menu)
