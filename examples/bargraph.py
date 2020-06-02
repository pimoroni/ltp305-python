import time
import math
import random
from ltp305 import LTP305


print("""bargraph.py - A basic graph example

Displays an animated rising/falling bar on the left matrix,
and a scrolling bar graph on the right.

Press Ctrl+C to exit!

""")

display = LTP305()
width, height = display.get_shape()

values = [0, 0, 0, 0, 0]


while True:
    # Add a new random value to our list and prune the list to visible values
    values.insert(0, random.randint(0, height))
    values = values[:width]

    # Animate a value from 0 to height + 1
    value = (math.sin(time.time() * math.pi) + 1) / 2.0
    value *= height + 1
    value = math.floor(value)

    for y in range(height):
        y = height - 1 - y

        for x in range(width // 2):
            # Left
            display.set_pixel(x, y, value <= y)

            # Right
            display.set_pixel(x + (width // 2), y, values[x] <= y)

    time.sleep(1.0 / height)
    display.show()
