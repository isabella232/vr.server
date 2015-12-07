import os
import shlex
import subprocess

from vr.common.utils import randchars


here = os.path.dirname(os.path.abspath(__file__))
os.environ['APP_SETTINGS_YAML'] = os.path.join(here, 'testconfig.yaml')


from django.contrib.auth.models import User


def sh(cmd):
    subprocess.call(shlex.split(cmd), stderr=subprocess.STDOUT)


def dbsetup():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    sql = os.path.join(here, 'dbsetup.sql')
    sh('psql -f %s -U postgres' % sql)

    # Now create tables
    manage = 'vr.server.manage'
    sh('python -m %s syncdb --noinput' % manage)
    sh('python -m %s migrate' % manage)


def randurl():
    return 'http://%s/%s' % (randchars(), randchars())


def get_user():
    u = User(username=randchars())
    u.set_password('password123')
    u.is_admin = True
    u.is_staff = True
    u.save()
    return u
