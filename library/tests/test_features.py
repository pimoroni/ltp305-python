import mock


def test_set_pixel(smbus):
    from ltp305 import LTP305, CMD_MATRIX_L, CMD_MATRIX_R
    display = LTP305()
    display.set_pixel(0, 0, 1)
    display.set_pixel(5, 0, 1)
    display.show()
    smbus.SMBus(1).write_i2c_block_data.assert_has_calls((
        mock.call(display.address, CMD_MATRIX_L, [1, 0, 0, 0, 0, 0, 0, 0]),
        mock.call(display.address, CMD_MATRIX_R, [1, 0, 0, 0, 0, 0, 0, 0])
    ))
    smbus.reset_mock()
    display.set_pixel(0, 0, 0)
    display.set_pixel(5, 0, 0)
    display.show()
    smbus.SMBus(1).write_i2c_block_data.assert_has_calls((
        mock.call(display.address, CMD_MATRIX_L, [0, 0, 0, 0, 0, 0, 0, 0]),
        mock.call(display.address, CMD_MATRIX_R, [0, 0, 0, 0, 0, 0, 0, 0])
    ))


def test_set_decimal(smbus):
    from ltp305 import LTP305, CMD_MATRIX_L, CMD_MATRIX_R
    display = LTP305()
    display.set_decimal(left=True, right=True)
    display.show()
    smbus.SMBus(1).write_i2c_block_data.assert_has_calls((
        mock.call(display.address, CMD_MATRIX_L, [0, 0, 0, 0, 0, 0, 0, 0b01000000]),
        mock.call(display.address, CMD_MATRIX_R, [0, 0, 0, 0, 0, 0, 0b10000000, 0])
    ))
    smbus.reset_mock()
    display.set_decimal(left=False, right=False)
    display.show()
    smbus.SMBus(1).write_i2c_block_data.assert_has_calls((
        mock.call(display.address, CMD_MATRIX_L, [0, 0, 0, 0, 0, 0, 0, 0]),
        mock.call(display.address, CMD_MATRIX_R, [0, 0, 0, 0, 0, 0, 0, 0])
    ))


def test_set_character(smbus):
    from ltp305 import LTP305, CMD_MATRIX_L, CMD_MATRIX_R
    display = LTP305()
    display.set_character(0, "A")
    display.set_character(5, "B")
    display.show()
    smbus.SMBus(1).write_i2c_block_data.assert_has_calls((
        mock.call(display.address, CMD_MATRIX_L, [126, 17, 17, 17, 126, 0, 0, 0]),
        mock.call(display.address, CMD_MATRIX_R, [15, 17, 17, 15, 17, 17, 15, 0])
    ))
