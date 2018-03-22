import functools

import six
from six.moves import urllib

import pytest
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import jaraco.context

from vr.common.utils import randchars
from vr.server.tests import get_user
from vr.server import models


def test_login_required():
    # Try to access the dashboard.  Should get redirected.
    c = Client()
    r = c.get(reverse('dash'))
    assert r.status_code == 302


def test_login(postgresql):
    u = get_user()
    url = reverse('login')
    c = Client()
    r = c.post(url, data={'username': u.username, 'password': 'password123'})
    # Should be redirected to homepage
    assert urllib.parse.urlsplit(r['Location']).path == '/'


expect_validation_error = (
    jaraco.context.null
    if six.PY3 else
    functools.partial(pytest.raises, ValidationError)
)
"""
On Python 2, xmlrpc raises validation errors, but on Python 3,
these structures seem to work, so only expect the validation
errors on Python 2.
"""


def test_config_ingredient_marshaling():
    ci = models.ConfigIngredient(
        name=randchars(),
        config_yaml='1: integer keys are not allowed in XMLRPC',
        env_yaml=None,
    )
    with expect_validation_error():
        ci.save()


def test_release_config_marshaling(postgresql):
    app = models.App(
        name=randchars(),
        repo_url=randchars(),
        repo_type='git'
    )
    app.save()
    b = models.Build(
        app=app,
        tag=randchars(),
    )
    b.save()
    release = models.Release(
        build=b,
        config_yaml=None,
        # numbers can only be 32 bit in xmlrpc
        env_yaml='FACEBOOK_APP_ID: 1234123412341234'
    )
    with expect_validation_error():
        release.save()


def test_swarm_config_marshaling(postgresql):
    app = models.App(
        name=randchars(),
        repo_url=randchars(),
        repo_type='git'
    )
    app.save()
    b = models.Build(
        app=app,
        tag=randchars(),
    )
    b.save()
    release = models.Release(
        build=b,
    )
    release.save()
    squad = models.Squad(name=randchars())
    squad.save()
    swarm = models.Swarm(
        app=app,
        release=release,
        config_name=randchars(),
        proc_name=randchars(),
        squad=squad,
        config_yaml='1: integer key!',
    )
    with expect_validation_error():
        swarm.save()
