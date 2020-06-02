import math
import time
import random


print("""eyes.py - They're watching you!

Press Ctrl+C to exit!

""")


from ltp305 import LTP305

display = LTP305()


def eye(x, y):
    display.set_pixel(x, y, True)
    display.set_pixel(x, y + 1, True)
    display.set_pixel(x + 1, y, True)
    display.set_pixel(x + 1, y + 1, True)


while True:
    t = time.time() * math.pi

    # Get eye x and y positions in the range 0.0 to 1.0
    # You can plug in your own 0.0 to 1.0 values here
    x = (math.sin(t / 2) + 1) / 2
    y = (math.sin(t / 4) + 1) / 2

    # Multiply them up to display coords and convert to itn
    x = math.floor(x * 4)
    y = math.floor(y * 6)

    # Clear the display
    display.clear()

    # Blink occasionally
    if not random.randint(0, 20) == 2:
        # Draw the eyes if not blinking
        eye(x, y)
        eye(x + 5, y)

    # Update the display at 10FPS
    # This gives our crude blink code time to not look like a random flicker
    display.show()
    time.sleep(1.0 / 10)
