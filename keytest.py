"""Print PicoCalc key names and VT100 sequences until Escape is pressed."""

from picocalc import keyboard


KEY_NAMES = {
    b"\x1b\x1b": "Escape",
    b"\r": "Enter",
    b"\t": "Tab",
    b"\x7f": "Backspace",
    b" ": "Space",
    b"\x1b[H": "Home",
    b"\x1b[F": "End",
    b"\x1b[3~": "Delete",
}

ARROWS = {
    "A": "Up",
    "B": "Down",
    "C": "Right",
    "D": "Left",
}

MODIFIERS = {
    "2": "Shift",
    "3": "Alt",
    "4": "Shift+Alt",
    "5": "Ctrl",
    "6": "Shift+Ctrl",
    "7": "Alt+Ctrl",
    "8": "Shift+Alt+Ctrl",
}

for code, name in ARROWS.items():
    KEY_NAMES[("\x1b[" + code).encode()] = name

    for modifier, modifier_name in MODIFIERS.items():
        sequence = ("\x1b[1;" + modifier + code).encode()
        KEY_NAMES[sequence] = modifier_name + "+" + name


def key_name(seq):
    """Return a readable name for one keyboard sequence."""
    name = KEY_NAMES.get(seq)
    if name:
        return name

    if len(seq) == 1:
        value = seq[0]

        if 32 <= value <= 126:
            return chr(value)

        if 1 <= value <= 26:
            return "Ctrl+" + chr(value + 64)

    # The keyboard driver encodes Alt+printable as Escape plus the character.
    if (
        len(seq) == 2
        and seq[0] == 0x1B
        and 32 <= seq[1] <= 126
    ):
        return "Alt+" + chr(seq[1])

    return "Unknown"


def keytest():
    buffer = bytearray(30)
    print("Press Escape to exit.")

    while True:
        count = keyboard.readinto(buffer)
        if not count:
            continue

        sequence = bytes(buffer[:count])
        print("Key: {:<20} VT100: {!r}".format(
            key_name(sequence), sequence
        ))

        # PicoKeyboard encodes Escape as two consecutive escape bytes.
        if b"\x1b\x1b" in sequence:
            break



keytest()
