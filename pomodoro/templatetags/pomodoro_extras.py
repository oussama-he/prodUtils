from django import template
from django.utils import timezone
from django.contrib.messages.constants import DEBUG, INFO, SUCCESS, WARNING, ERROR

register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.filter(name='format_date')
def format_date(value):
    if not isinstance(value, type(timezone.now())) or value is None:
        return '-'

    if value.date() == timezone.now().date():
        return 'Today at %s' % value.strftime('%H:%M')
    elif (value.date() - timezone.now().date()).days == -1:
        return 'Yesterday at %s' % value.strftime('%H:%M')
    else:
        if value.date().year < timezone.now().year:
            return value.strftime("%b %d '%y at %H:%M")
        else:
            return value.strftime('%a %d %b at %H:%M')


@register.filter
def message_heading(level: int):
    if level == DEBUG:
        return "Debugging."
    elif level == INFO:
        return "Info."
    elif level == SUCCESS:
        return "Congratulation."
    elif level == WARNING:
        return "Warning."
    elif level == ERROR:
        return "Error."
    return ""


@register.filter(name='format_duration')
def format_duration(value: int) -> str:
    try:
        value = int(value)
    except ValueError:
        return str(value)

    if value < 59:
        return f'{value:02d}s'
    elif value < 3600:
        mins, secs = divmod(value, 60)
        return f'{mins:02d}m {secs:02d}s'
    else:
        mins, secs = divmod(value, 60)
        hrs, mins = divmod(mins, 60)
        return f'{hrs:02d}h {mins:02d}m'
