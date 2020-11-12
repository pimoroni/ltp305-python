import smbus
from .font import font


__version__ = '0.0.1'


MODE = 0b00011000
OPTS = 0b00001110  # 1110 = 35mA, 0000 = 40mA

CMD_BRIGHTNESS = 0x19
CMD_MODE = 0x00
CMD_UPDATE = 0x0C
CMD_OPTIONS = 0x0D

CMD_MATRIX_L = 0x0E
CMD_MATRIX_R = 0x01


class LTP305:
    """
    _buf_matrix_left = [
    # Row  7654321
        0b01111111,  # col 1, bottom = msb
        0b01111111,  # col 2
        0b01111111,  # col 3
        0b01111111,  # col 4
        0b01111111,  # col 5
        0b00000000,
        0b00000000,
        0b01000000   # bit 7 = decimal dot
    ]

    _buf_matrix_right = [
    # Col    12345
        0b00011111,  # row 1
        0b00011111,  # row 2
        0b00011111,  # row 3
        0b00011111,  # row 4
        0b00011111,  # row 5
        0b00011111,  # row 6
        0b10011111,  # row 7 + bit 8 = decimal dot
        0b00000000
    ]
    """

    def __init__(self, address=0x61, brightness=0.5):
        """LTP305 5x7 x 2 Matrix Driver

        :param address: i2c address, one of 0x61, 0x62 or 0x63 (default 0x61)
        :param brightness: LED brightness from 0.0 to 1.0 (default 0.5)

        """
        self.bus = smbus.SMBus(1)
        self.address = address
        self.set_brightness(brightness)
        self.clear()

    def clear(self):
        """Clear both LED matrices.

        Must call .show() to display changes.

        """
        self._buf_matrix_left = [0 for _ in range(8)]
        self._buf_matrix_right = [0 for _ in range(8)]

    def set_brightness(self, brightness, update=False):
        """Set brightness of both LED matrices.

        :param brightnes: LED brightness from 0.0 to 1.0
        :param update: Push change to display immediately (otherwise you must call .show())

        """
        self._brightness = int(brightness * 127.0)
        self._brightness = min(127, max(0, self._brightness))
        if update:
            self.bus.write_byte_data(self.address, CMD_BRIGHTNESS, self._brightness)

    def set_decimal(self, left=None, right=None):
        """Set decimal of left and/or right matrix.

        :param left: State of left decimal dot
        :param right: State of right decimal dot

        """
        if left is not None:
            if left:
                self._buf_matrix_left[7] |= 0b01000000
            else:
                self._buf_matrix_left[7] &= 0b10111111
        if right is not None:
            if right:
                self._buf_matrix_right[6] |= 0b10000000
            else:
                self._buf_matrix_right[6] &= 0b01111111

    def set_pixel(self, x, y, c):
        """Set a single pixel on the matrix.

        :param x: x position from 0 to 9 (0-4 on left matrix, 5-9 on right)
        :param y: y position
        :param c: state on/off

        """
        if x < 5:  # Left Matrix
            if c:
                self._buf_matrix_left[x] |= (0b1 << y)
            else:
                self._buf_matrix_left[x] &= ~(0b1 << y)
        else:      # Right Matrix
            x -= 5
            if c:
                self._buf_matrix_right[y] |= (0b1 << x)
            else:
                self._buf_matrix_right[y] &= ~(0b1 << x)

    def set_character(self, x, char):
        """Set a single character.

        :param x: x position, 0 for left, 5 for right, or in between if you fancy
        :param char: string character or char ordinal

        """
        if type(char) is not int:
            char = ord(char)
        char = font[char]
        for cx in range(5):
            for cy in range(8):
                c = char[cx] & (0b1 << cy)
                self.set_pixel(x + cx, cy, c)

    def get_shape(self):
        """Set the width/height of the display."""
        return 10, 7

    def set_image(self, image, offset_x=0, offset_y=0, wrap=False, bg=0):
        """Set a PIL image to the display buffer."""
        image_width, image_height = image.size

        if image.mode != "1":
            image = image.convert("1")

        display_width, display_height = self.get_shape()

        for y in range(display_height):
            for x in range(display_width):
                p = bg
                i_x = x + offset_x
                i_y = y + offset_y
                if wrap:
                    while i_x >= image_width:
                        i_x -= image_width
                    while i_y >= image_height:
                        i_y -= image_height
                if i_x < image_width and i_y < image_height:
                    p = image.getpixel((i_x, i_y))
                self.set_pixel(x, y, p)

    def show(self):
        """Update the LED matrixes from the buffer."""
        self.bus.write_i2c_block_data(self.address, CMD_MATRIX_L, self._buf_matrix_left)
        self.bus.write_i2c_block_data(self.address, CMD_MATRIX_R, self._buf_matrix_right)
        self.bus.write_byte_data(self.address, CMD_MODE, MODE)
        self.bus.write_byte_data(self.address, CMD_OPTIONS, OPTS)
        self.bus.write_byte_data(self.address, CMD_BRIGHTNESS, self._brightness)
        self.bus.write_byte_data(self.address, CMD_UPDATE, 0x01)


if __name__ == "__main__":
    import time
    matrix = LTP305(0x61)
    delay = 1.0 / 72 * 4
    c = True
    while True:
        for n in range(10):
            matrix.set_character(0, str(n))
            matrix.set_character(5, 'abcdefghij'[n])
            matrix.show()
            time.sleep(0.1)

        matrix.set_character(0, "=")
        matrix.set_character(5, ")")
        matrix.show()
        time.sleep(1.0)

        matrix.clear()
        matrix.show()
        time.sleep(0.5)

        for _ in range(2):
            for y in range(7):
                for x in range(10):
                    matrix.set_pixel(x, y, c)
                    matrix.show()
                    time.sleep(delay)

            matrix.set_decimal(left=c)
            matrix.show()
            time.sleep(delay)

            matrix.set_decimal(right=c)
            matrix.show()
            time.sleep(delay)
            c = not c
