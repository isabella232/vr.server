import tempfile

import pytest

import django
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.files import File

from vr.server import models
from vr.server.tests import randurl
from vr.common.utils import randchars


pytestmark = pytest.mark.usefixtures('postgresql')


@pytest.fixture(scope="module", autouse=True)
def rewrite_default_file_storage(gridfs):
    """
    By the time these tests run, django has already started up
    and configured the default_storage for files, binding the
    GridFSStorage to the default host/port. But the test suite
    has gone to a lot of trouble to supply an ephemeral instance
    of MongoDB, so re-init the default storage to use that
    instance.
    """
    django.core.files.base.default_storage.__init__()


def test_build_usable(gridfs):
    app_url = randurl()
    a = models.App(name=randchars(), repo_url=app_url, repo_type='hg')
    a.save()
    with somefile() as f:
        b = models.Build(
            app=a,
            tag='blah',
            start_time=timezone.now() - relativedelta(minutes=2),
            end_time=timezone.now() - relativedelta(minutes=1),
            file=File(f),
            status='success',
        )
        b.save()
    assert b.is_usable() == True


def test_build_unusable_status(gridfs):
    app_url = randurl()
    a = models.App(name=randchars(), repo_url=app_url, repo_type='hg')
    a.save()
    with somefile() as f:
        b = models.Build(
            app=a,
            tag='blah',
            start_time=timezone.now() - relativedelta(minutes=2),
            end_time=timezone.now() - relativedelta(minutes=1),
            file=File(f),
            status='',
        )
        b.save()
    assert b.is_usable() == False


class somefile():
    def __enter__(self):
        self.file = tempfile.NamedTemporaryFile()
        return self.file

    def __exit__(self, type, value, traceback):
        self.file.close()

