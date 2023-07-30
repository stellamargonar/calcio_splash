from datetime import datetime, timezone

from django import template

register = template.Library()


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    if key:
        return dict_data.get(key)


@register.filter('milliseconds')
def milliseconds(timestamp):
    if timestamp is None:
        return None
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (timestamp - epoch).total_seconds() * 1000.0


@register.filter('multiply')
def multiply(a, b):
    return a * b
