import atexit
import os
import readline
import rlcompleter

# TAB complete
readline.parse_and_bind("tab: complete")

# Store interactive Python shell history in ~/.cache/python/history
history_file = os.path.join(
    os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
    "python/history",
    )
try:
    readline.read_history_file(history_file)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, history_file)

# cleanup
del os, history_file, readline, rlcompleter, atexit

