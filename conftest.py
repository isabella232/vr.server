from django import setup

from vr.server.tests import dbsetup


def pytest_configure():
    """
    Setup the django instance before to run the tests

    Starting from django 1.7 we need to let django to setup itself.
    """

    setup()


def pytest_addoption(parser):
    parser.addoption('--nodb', action='store_true',
            default=False,
            help="Don't destroy/create DB")


def pytest_sessionstart(session):
    if not session.config.option.nodb:
        dbsetup()
