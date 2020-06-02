# Pimoroni LTP305 LED Matrices Breakout <!-- omit in toc -->

The LTP305 breakout includes two LTP305 displays and an i2c dual matrix driver to drive them.

- [Getting Started](#getting-started)
  - [Pre-requisites](#pre-requisites)
    - [Python 3 & pip](#python-3--pip)
    - [Enabling i2c](#enabling-i2c)
  - [Installing the library](#installing-the-library)
- [Reference](#reference)
  - [set_pixel](#set_pixel)
  - [set_decimal](#set_decimal)
  - [set_character](#set_character)
  - [set_image](#set_image)
  - [get_shape](#get_shape)
  - [clear](#clear)
  - [show](#show)

## Getting Started

You'll need to install the LTP305 software library and enable i2c on your Raspberry Pi.

### Pre-requisites

#### Python 3 & pip

You should use Python 3, which may need installing on your Pi:

```
sudo apt update
sudo apt install python3 python3-pip
```

#### Enabling i2c

You can use `sudo raspi-config` on the command line, the GUI Raspberry Pi Configuration app from the Pi desktop menu, or use the following command to enable i2c:

```
sudo raspi-config nonint do_i2c 0
```

### Installing the library

```python
python3 -m pip install ltp305
```

## Reference

In all cases you'll want to create an instance of the LTP305 class with the appropriate i2c address for your device.

The following addresses are available:

* `0x61` - Default address
* `0x62` - Solder bridge applied to Addr+1
* `0x63` - Cut Addr+2

```python
from ltp305 import LTP305
display = LTP305(address=0x61)
```

### set_pixel

Set a single pixel. Treats both matrices as a single display that's 10 pixels wide and 7 pixels high.

```python
display.set_pixel(0, 0, 1)
display.show()
```

### set_decimal

Set the decimal dot on one or both matrix displays:

```python
display.set_decimal(left=True, right=False)  # Just the left
display.set_decimal(left=False, right=True)  # Just the right
display.set_decimal(left=True, right=True)   # Both
display.show()
```

### set_character

The library includes a font with a range of ASCII and Unicode characters, each matrix can display a single character.

```python
display.set_character(0, "a")
display.set_character(5, "b")
display.show()
```

### set_image

Set a 1-bit PIL image to the display.

```python
from PIL import Image, ImageDraw
image = Image.new("1", display.get_shape())
draw = ImageDraw.draw(image)
draw.rectangle((0, 0, 4, 6), 1)
display.set_image(image)
display.show()
```

### get_shape

Return the width and height of the display:

```python
width, height = display.get_shape()
```

### clear

Clear the display. Sets all pixels in the buffer to 0 (off). You must call `show()` to update the display.

```python
display.clear()
```

### show

Once you've finished setting pixels or drawing characters into the buffer, you must call `show` to update the matrices with the buffer:

```python
display.show()
```