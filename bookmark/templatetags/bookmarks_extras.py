from django import template
from urllib.parse import urlparse


register = template.Library()


@register.filter
def get_host_name(value):
    parsed_url = urlparse(value)
    return parsed_url.hostname

