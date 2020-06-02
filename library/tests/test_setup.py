def test_setup(smbus):
    import ltp305
    display = ltp305.LTP305()
    smbus.SMBus.assert_called_with(1)
    del display
