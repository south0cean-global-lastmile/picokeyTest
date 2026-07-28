"""Print PicoCalc key presses until Escape is pressed."""

from picocalc import keyboard


def run():
    buffer = bytearray(30)
    print("Press Escape to exit.")

    while True:
        count = keyboard.readinto(buffer)
        if not count:
            continue

        keys = bytes(buffer[:count])
        print("Key:", keys)

        # PicoKeyboard encodes Escape as two consecutive escape bytes.
        if b"\x1b\x1b" in keys:
            break


# PicoCalc's script launcher does not necessarily set __name__ to "__main__".
run()
