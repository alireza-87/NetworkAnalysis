from __future__ import print_function
import collections
from colors import Colors
import builtins as __builtin__

log = open("log1.txt", "a")
save_log = False


def save(is_save):
    save_log = is_save


def print(*args):
    if save_log:
        new_line = ""
        for item in args:
            item_clean = str(item).replace(Colors.ENDC, '')
            item_clean = item_clean.replace(Colors.BOLD, '')
            item_clean = item_clean.replace(Colors.OKGREEN, '')
            item_clean = item_clean.replace(Colors.OKBLUE, '')
            item_clean = item_clean.replace(Colors.FAIL, '')
            item_clean = item_clean.replace(Colors.OKCYAN, '')
            item_clean = item_clean.replace(Colors.WARNING, '')
            item_clean = item_clean.replace(Colors.HEADER, '')
            item_clean = item_clean.replace(Colors.UNDERLINE, '')
            new_line = new_line + item_clean + "\n"
        new_line = (new_line + """""")
        log.write(new_line)
        log.flush()
    __builtin__.print(*args)
