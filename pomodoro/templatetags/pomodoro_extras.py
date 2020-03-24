from django import template
from django.utils import timezone


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
def get_at_index(list, index):
    return list[index]


@register.filter(name='format_duration')
def format_duration(value: int) -> str:
    value = int(value)
    if value < 59:
        return f'{value:02d}s'
    elif value < 3600:
        mins, secs = divmod(value, 60)
        return f'{mins:02d}m {secs:02d}s'
    else:
        mins, secs = divmod(value, 60)
        hrs, mins = divmod(mins, 60)
        return f'{hrs:02d}h {mins:02d}m'


# @register.filter(name='get_due_date_string')
# def get_due_date_string(value):
#     delta = value - date.today()
#
#     if delta.days == 0:
#         return "Today!"
#     elif delta.days < 1:
#         return "%s %s ago!" % (abs(delta.days),
#             ("day" if abs(delta.days) == 1 else "days"))
#     elif delta.days == 1:
#         return "Tomorrow"
#     elif delta.days > 1:
#         return "In %s days" % delta.days