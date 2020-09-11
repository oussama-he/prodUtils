import datetime
import os
from datetime import timedelta

from django.utils import timezone

from .models import Session


def get_week_range() -> tuple:
    today = timezone.now().date()
    # My week starts on Sunday
    start_week = today - timedelta((today.weekday() + 1) % 7)
    end_week = start_week + timedelta(days=6)
    return start_week, end_week


def get_last_week_days() -> list:
    days = list()
    week_range = get_week_range()
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


def get_tasks_from_sessions(session_qs) -> dict:
    tasks = dict()
    for session in session_qs:
        tasks[session.task] = dict(duration=0, interrupted=0, continued=0)
    return tasks


def get_session_info_of_tasks(session_qs) -> dict:
    tasks = get_tasks_from_sessions(session_qs)
    for session in session_qs:
        tasks[session.task]['duration'] += session.get_duration()
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
#
# base_dir = "/home/oussama/Desktop/الفلاش_الدعوي"
# result = os.scandir(base_dir)
# dirs_files = dict()


def sort_entries(entries):
    dirs = []
    files = []
    for entry in entries:
        if entry.is_dir():
            dirs.append(entry)
        elif entry.is_file():
            files.append(entry)
    dirs.sort(key=str)
    files.sort(key=str)
    return files + dirs

files = list()
def list_files_name(base_dir, entries, sep=''):

    entries = sort_entries(entries)
    for entry in entries:
        if entry.is_dir():
            print(entry.name, sep)
            files.append([entry.name, 'dir'])
            base_dir = os.path.join(base_dir, entry.name)
            entries = os.scandir(base_dir)
            sep += '    '
            list_files_name(base_dir, entries, sep)
            base_dir = os.path.split(base_dir)[0]
            sep = sep[:len(sep)-4]

        elif entry.is_file():
            file_name = os.path.splitext(entry.name)[0]
            files.append([file_name, 'file'])
            print(os.path.splitext(entry.name)[0], sep)
    return files

# list_files_name(entries=result)
# print(">>>>>>>>>>>>>>", files[][0])
