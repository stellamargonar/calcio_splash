from fabric.api import run
from fabric.context_managers import cd, prefix, shell_env
from fabric.contrib.project import rsync_project
from fabric.decorators import with_settings
from fabric.state import env

from fabfile.utils import settings_from_json

s = settings_from_json()


@with_settings(**s)
def code_update_local():
    """ update remote code by copying from local"""
    rsync_project(env.remote_path, './', exclude=['.git', '.idea', '__pycache__'])


@with_settings(**s)
def code_update_git():
    """ update remote code by copying from git"""
    with cd(env.remote_path):
        run("git fetch --all")
        run("git reset --hard origin/master")


@with_settings(**s)
def dependencies_update():
    """ update python dependencies"""
    with cd(env.remote_path):
        run("poetry install --no-dev")


@with_settings(**s)
def db_migrate():
    """ apply DB migrations"""
    with cd(env.remote_path), shell_env(DJANGO_EXTRA_SETTINGS=env.django_extra_settings):
        run("poetry run python manage.py migrate")


@with_settings(**s)
def statics_update():
    """ publish updated static files to the configured storage"""
    with cd(env.remote_path), shell_env(DJANGO_EXTRA_SETTINGS=env.django_extra_settings):
        run("poetry run python manage.py collectstatic --no-input")


@with_settings(**s)
def webserver_restart():
    """ restart uwsgi"""
    run("touch {}".format(env.uwsgi_conf_path))


@with_settings(**s)
def deploy(mode='git'):
    """ full deploy; by default use git code"""
    assert mode in {'local', 'git'}, 'Invalid mode: {}; select between "local" and "git" (the default)'.format(mode)

    if mode == 'local':
        code_update_local()
    else:
        code_update_git()

    dependencies_update()
    db_migrate()
    statics_update()
    webserver_restart()


@with_settings(**s)
def deploy_local():
    """ full deploy, using local code"""
    deploy(mode='local')


@with_settings(**s)
# [sp] usage: fab manage:command=showmigrations
def manage(command):
    """ execute a generic python manage.py <command>"""
    with cd(env.remote_path), shell_env(DJANGO_EXTRA_SETTINGS=env.django_extra_settings):
        run("poetry run python manage.py " + command)
