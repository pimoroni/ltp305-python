import sys
import mock
import pytest


@pytest.fixture(scope='function', autouse=True)
def cleanup():
    """Force module reimport between tests."""
    yield None
    try:
        del sys.modules['ltp305']
    except KeyError:
        pass


@pytest.fixture(scope='function', autouse=False)
def smbus():
    """Mock smbus module."""
    smbus = mock.MagicMock()
    sys.modules['smbus'] = smbus
    yield smbus
    del sys.modules['smbus']
