from pxm.version import pxm_version


def test_version_availability():
    assert pxm_version != '0.0.0', 'expected application version, got default placeholder instead'
