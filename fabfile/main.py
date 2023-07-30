import json

from fabric import task

with open("fabfile/settings-default.json") as f:
    config = json.load(f)

try:
    with open("fabfile/settings-local.json") as f:
        config.update(json.load(f))
except FileNotFoundError:
    pass


env = {
    "DJANGO_EXTRA_SETTINGS": config["django_extra_settings"],
    "PATH": "/home/ubuntu/.local/bin/:$PATH",
}


@task(hosts=config["hosts"])
def code_update_git(c):
    """update remote code by copying from git"""
    with c.cd(config['remote_path']):
        c.run("git fetch --all", env=env)
        c.run("git reset --hard origin/master", env=env)


@task()
def code_update_local(c):
    """update remote code by copying from local"""
    raise NotImplemented("Not yet, rsync should be migrated")
    # rsync_project(env.remote_path, './', exclude=['.git', '.idea', '__pycache__'])


@task(hosts=config["hosts"])
def dependencies_update(c):
    """update python dependencies"""
    with c.cd(config['remote_path']):
        c.run("poetry install --only main", env=env)


@task(hosts=config["hosts"])
def db_migrate(c):
    with c.cd(config['remote_path']):
        c.run("poetry run python manage.py migrate", env=env)


@task(hosts=config["hosts"])
def statics_update(c):
    """publish updated static files to the configured storage"""
    with c.cd(config['remote_path']):
        c.run("poetry run python manage.py collectstatic --no-input", env=env)


@task(hosts=config["hosts"])
def webserver_restart(c):
    """restart uwsgi"""
    c.run("touch {}".format(config['uwsgi_conf_path']))


@task(code_update_git, dependencies_update, db_migrate, statics_update, webserver_restart)
def deploy(c):
    """full deploy; by default use git code"""
    pass


@task(code_update_local, dependencies_update, db_migrate, statics_update, webserver_restart)
def deploy_local(c):
    """update remote code by copying from local"""
    pass


# [sp] usage: fab manage showmigrations
@task(hosts=config["hosts"])
def manage(c, command):
    with c.cd(config['remote_path']):
        c.run("poetry run python manage.py " + command, env=env)


@task(hosts=config["hosts"])
def download_db(c):
    c.get("/var/www/db/calcio_splash.db", "db.sqlite3")
