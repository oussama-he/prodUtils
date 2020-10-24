import datetime
from datetime import timedelta
import tempfile

from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML

from .models import Session


def render_html_to_pdf(html):
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def generate_html_from_template(template: str, context: dict, request):
    html_string = render_to_string(template, context=context, request=request)
    return HTML(string=html_string, base_url=request.build_absolute_uri())


def get_last_week_range() -> tuple:
    today = timezone.now().date()
    # My week starts on Sunday
    start_week = today - timedelta((today.weekday() + 1) % 7)
    end_week = start_week + timedelta(days=6)
    return start_week, end_week


def get_last_week_days() -> list:
    days = list()
    week_range = get_last_week_range()
    start_week = week_range[0]
    days.append(start_week)
    for i in range(1, 7):
        day = start_week + timedelta(days=i)
        days.append(day)
    return days


def get_last_month_days_until_today() -> list:
    today_date = datetime.date.today()
    year = today_date.year
    month = today_date.month
    return [datetime.date(year, month, day) for day in range(1, today_date.day + 1)]


def get_sessions_stats(session_qs) -> dict:
    stats = dict(total_duration=0, session_count=0, continued=0, interrupted=0, avg_duration=0)
    for session in session_qs:
        stats['total_duration'] += session.get_duration()
        if session.interrupted:
            stats['interrupted'] += 1
        else:
            stats['continued'] += 1
    stats['session_count'] = stats['continued'] + stats['interrupted']
    if stats['session_count']:
        stats['avg_duration'] = stats['total_duration'] / stats['session_count']
    return stats


def get_tasks_from_sessions(session_qs) -> dict:
    tasks = dict()
    for session in session_qs:
        tasks[session.task] = dict(duration=0, interrupted=0, continued=0, session_count=0)
    return tasks


def get_session_info_of_tasks(session_qs) -> dict:
    tasks = get_tasks_from_sessions(session_qs)
    for session in session_qs:
        tasks[session.task]['duration'] += session.get_duration()
        tasks[session.task]['session_count'] += 1
        if session.interrupted:
            tasks[session.task]['interrupted'] += 1
        else:
            tasks[session.task]['continued'] += 1

    return tasks


def get_tasks_info_of_day(day) -> dict:
    session_qs = Session.objects.filter(start_time__date=day)
    result = dict(tasks=list(), total_duration=0, interrupted=0, continued=0, session_count=0, avg_duration=0)

    if not session_qs.count():
        return result

    tasks = get_session_info_of_tasks(session_qs)

    for key, value in tasks.items():
        result['interrupted'] += value['interrupted']
        result['continued'] += value['continued']
        result['total_duration'] += value['duration']
        result['tasks'].append({
            'project': key.project,
            'task': key,
            'sessions': {**value}
        })
    result['session_count'] = result['interrupted'] + result['continued']
    result['avg_duration'] = result['total_duration'] / result['session_count']

    return result


def get_tasks_info_of_days(days: list) -> dict:
    day_tasks_info = dict()
    for day in days:
        day_tasks_info[day] = get_tasks_info_of_day(day)
    return day_tasks_info


def get_result_stats(tasks_info) -> dict:
    result = dict(continued=0, interrupted=0, total_duration=0, avg_duration=0)
    for info in tasks_info.values():
        result['continued'] += info['continued']
        result['interrupted'] += info['interrupted']
        result['total_duration'] += info['total_duration']
    result['session_count'] = result['continued'] + result['interrupted']
    result['avg_duration'] = result['total_duration'] / result['session_count']
    result['days'] = tasks_info
    return result


def get_month_stats(month: int, year=None) -> dict:
    if not year:
        year = timezone.now().date().year

    stats = dict(continued=0, interrupted=0, duration=0, avg_duration=0, sessions=0, tasks=0, project=0)
    sessions = Session.objects.filter(start_time__date__month=month, start_time__date__year=year)
    # I use the expression below instead of this:
    # Task.objects.filter(last_activity__date__month=month, last_activity__date__year=year).count()
    # because last_activity field of some task entries not updated
    stats['tasks'] = sessions.values_list('task__id').distinct().count()
    stats['projects'] = sessions.values_list('task__project__id', flat=True).distinct().count()
    for session in sessions:
        stats['duration'] += session.get_duration()
        if session.interrupted:
            stats['interrupted'] += 1
        else:
            stats['continued'] += 1
    stats['sessions'] = stats['continued'] + stats['interrupted']
    stats['avg_duration'] = stats['duration'] / stats['sessions']
    return stats


def get_last_year_stats():
    stats = dict(months=dict(), total_duration=0, continued=0, interrupted=0, avg_duration=0)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    passed_months = [i for i in range(1, timezone.now().date().month+1)]

    for month_int, month_str in zip(passed_months, months):
        stats['months'][month_str] = get_month_stats(month_int)

    for month in stats['months'].values():
        stats['total_duration'] += month['duration']
        stats['continued'] += month['continued']
        stats['interrupted'] += month['interrupted']
    stats['session_count'] = stats['continued'] + stats['interrupted']
    stats['avg_duration'] = stats['total_duration'] / stats['session_count']

    return stats
