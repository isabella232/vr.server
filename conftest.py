import os
import sys

import pytest
from django import setup

from vr.server.tests import dbsetup


def _path_hack():
    """
    hack the PYTHONPATH to ensure that re-entrant processes
    have access to packages loaded by pytest-runner.
    """
    os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)


def pytest_configure():
    """
    Setup the django instance before to run the tests

    Starting from django 1.7 we need to let django to setup itself.
    """
    _path_hack()
    setup()


@pytest.fixture
def gridfs(mongodb_instance):
    from django.conf import settings
    settings.GRIDFS_PORT = mongodb_instance.port


def pytest_addoption(parser):
    parser.addoption('--nodb', action='store_true',
            default=False,
            help="Don't destroy/create DB")


def pytest_sessionstart(session):
    if not session.config.option.nodb:
        dbsetup()
