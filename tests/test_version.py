from pxm.settings import APP_VERSION


def test_version_availability():
    assert APP_VERSION != 'unknown', 'expected application version, got default placeholder instead'
