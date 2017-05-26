import json
import os
from contextlib import contextmanager

from fabric.context_managers import prefix
from fabric.state import env


def _settings_from_json_file(path, fail_silently=False):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        if fail_silently:
            return dict()
        raise


def settings_from_json():
    s = {}
    s.update(_settings_from_json_file('fabfile/settings-default.json'))
    s.update(_settings_from_json_file('fabfile/settings-local.json', fail_silently=True))

    return s


@contextmanager
def venv():
    with prefix('source {}'.format(os.path.join(env.virtualenv_path, 'bin/activate'))):
        yield
