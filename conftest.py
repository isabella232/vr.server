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
    settings.MONGODB_URL = mongodb_instance.get_uri() + '/velociraptor'


@pytest.fixture
def postgresql(postgresql_instance, request):
    from django.conf import settings
    settings.DATABASES['default']['PORT'] = str(postgresql_instance.port)
    dbsetup(postgresql_instance.port)


@pytest.fixture()
def redis():
    try:
        redis = __import__('redis')
        redis.StrictRedis(host='localhost', port=6379).echo('this')
    except Exception as exc:
        tmpl = "Unable to establish connection to redis ({exc})"
        pytest.skip(tmpl.format(**locals()))
