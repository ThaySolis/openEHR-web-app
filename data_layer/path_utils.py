# Get the path to the main module.
# Based on <https://stackoverflow.com/a/1676860> and <https://stackoverflow.com/a/248862>
import sys, os
main_module = sys.modules["__main__"]
base_path = os.path.dirname(os.path.abspath(main_module.__file__))

def relative_path(*args):
    return os.path.join(base_path, *args)
