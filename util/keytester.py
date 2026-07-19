from readchar import readkey

from wizlib.ui.shell import ESC

while True:
    key = readkey()
    if key == ESC + '[1;':
        key = key + readkey() + readkey()
    print(" ".join(hex(ord(c)) for c in key))
