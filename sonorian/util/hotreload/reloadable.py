# TODO(joey): Add an abstract class for reloable objects.
# The interface will ideally look like:
#
#   inst.dump() -> state
#       Return a serializable state that can be loaded.
#   klass.load(state) -> Object
#       Load and initialize an object from serializable state.
#   inst.reload_children()
#       Reload all owned objects.It would be nice if this was
#       intelligent about the files that were changed.
