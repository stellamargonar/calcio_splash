# Development

## How to Setup
Better using [asdf](https://asdf-vm.com/):

```
$ asdf install
$ poetry shell
$ poetry install
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
$ $EDITOR ~/.ssh/config
# add something like this:
Host <your-host>
    IdentityFile ~/.ssh/fuoriposto-master.pem
    User ubuntu
```

Remember to also edit the `settings-default.json` according to your configuration, if you didn't use our own.

Once everything is in place, you can deploy the git `master` code with:
```
$ fab deploy
```

If you want instead to publish in production your own local code (risky, but it might be needed to test a few things,
or to quickly deploy an hotfix) you can use:
```
$ fab deploy-local
```

Both scripts will:
* upload the new code on the server (either from GIT or from your local repo with `rsync`);
* update the virtualenv by installing (new) dependencies;
* apply migrations to the DB;
* update the static files;
* restart the uWSGI server

## How to Back-Up

It's better to backup both database and custom configuration. This project ships with `django-dbbackup`, you can
configure it in your server-side configuration and use it to backup your data in any storage supported by django;
to backup your configuration, you can use `rsync` or anything you like; glue everything together with `crontab`
and you'll be okay.

If you want to use S3, for example, this would be your settings:

```
DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': AWS_ACCESS_KEY_ID,
    'secret_key': AWS_SECRET_ACCESS_KEY,
    'bucket_name': AWS_BACKUP_BUCKET,
    'location': 'db',
}
```

This is what you want to add to your crontab:
```
export DJANGO_EXTRA_SETTINGS="/path/to/custom/conf.py" && cd /var/www/calcio_splash >/dev/null && source /var/www/venv/calcio_splash/bin/activate && python manage.py dbbackup
aws s3 cp --recursive /path/to/conf/ s3://aws_backup_bucket/conf/ --exclude *.pyc --exclude '*~'
```

# Goodies

You can run management commands with `fab`; if you want to create a superuser, for example, you can simply:
```
$ fab manage createsuperuser
```

Be aware, though, that to pass parameters you have to enclose the whole command between doublequotes:
```
$ fab manage "createsuperuser --help"
```
