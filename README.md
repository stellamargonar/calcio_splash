# Development

## How to Setup
Better using virtualenv:

```
$ mkvirtualenv calcio_spash
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

## How to Run
Currently we're using sqlite, no fancy-stuff 😊; First, apply migrations, then run the dev server:

```
$ python manage.py migrate
$ python manage.py runserver
```


# Deployment

## First Deployment
Deployment is made easy(-ier) with fabric; you can configure the server according to your own taste, we love the
nginx + uWSGI emperor/vassals combo. We configured it like this:
```
/var/www/calcio_splash                     # the root of the project
/var/www/conf/calcio_splash.ini            # uWSGI configuration file (linked into `/etc/uwsgi-emperor/vassals/`)
/var/www/conf/calcio_splash_settings.py    # production settings, used with DJANGO_EXTRA_SETTINGS
/var/www/db/calcio_splash.db               # sqlite3 DB
/var/www/venv                              # python virtualenv
```

## How to re-deploy
Once you're done, you can automate a few steps with [fabric](http://www.fabfile.org); it works through a couple of
configuration files: `fabfile/settings-default.json` and `fabfile/settings-local.json`; the latter will not be pushed
to git (it's ignored in `.gitignore`) and is therefore convenient to store private settings. We are providing an
example file you can use:
```
$ cp fabfile/settings-local.json.example fabfile/settings-local.json
$ $EDITOR fabfile/settings-local.json
```

Remember to also edit the `settings-default.json` according to your configuration, if you didn't use our own.

Once everything is in place, you can deploy the git `master` code with:
```
$ fab deploy
```

If you want instead to publish in production your own local code (risky, but it might be needed to test a few things,
or to quickly deploy an hotfix) you can use:
```
$ fab deploy_local
```

Both scripts will:
* upload the new code on the server (either from GIT or from your local repo with `rsync`);
* update the virtualenv by installing (new) dependencies;
* apply migrations to the DB;
* update the static files;
* restart the uWSGI server

# Goodies

You can run management commands with `fab`; if you want to create a superuser, for example, you can simply:
```
$ fab manage:createsuperuser
```

Be aware, though, that to pass parameters you have to enclose the whole command between doublequotes:
```
$ fab manage:"createsuperuser --help"
```
