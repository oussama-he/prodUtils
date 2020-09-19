import datetime

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.generic import UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pomodoro.models import Task, Session, Project
from .forms import NewTaskForm, NewProjectForm, EditSessionForm, EditTaskForm
from datetime import timedelta

from .utils import (
    get_sessions_stats,
    get_tasks_info_of_day,
    get_last_week_days,
    get_tasks_info_of_days,
    get_result_stats,
    get_last_month_days_until_today, get_last_year_stats, get_last_week_range
)

TIMEOUT_WORK = 25


def get_all_projects(request):
    projects = Project.objects.all()
    project_count = projects.count()
    total_duration = 0
    tasks_count = 0
    for project in projects:
        for task in project.task_set.all():
            total_duration += task.duration
            tasks_count += 1

    paginator = Paginator(projects, 25)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'pomodoro/all-projects.html', {
        "projects": projects,
        "project_count": project_count,
        "total_duration": total_duration,
        "tasks_count": tasks_count,
        "paginator": paginator
})


def home(request):
    recent_tasks = Task.objects.all()[:7]
    stats = dict()
    today = timezone.now()

    today_sessions = Session.objects.filter(start_time__date=today.date())
    stats['today'] = get_sessions_stats(today_sessions)

    yesterday_sessions = Session.objects.filter(start_time__date=today.date()-timedelta(1))
    stats['yesterday'] = get_sessions_stats(yesterday_sessions)

    last_week_sessions = Session.objects.filter(start_time__range=get_last_week_range())
    stats['last week'] = get_sessions_stats(last_week_sessions)

    last_month_sessions = Session.objects.filter(start_time__month=today.month, start_time__year=today.year)
    stats['last month'] = get_sessions_stats(last_month_sessions)

    last_year_sessions = Session.objects.filter(start_time__year=today.year)
    stats['last year'] = get_sessions_stats(last_year_sessions)

    return render(request, 'pomodoro/home.html', {'recent_tasks': recent_tasks, 'stats': stats})


def new_task(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('/pomodoro/home')
    else:
        form = NewTaskForm()

    return render(request, 'pomodoro/new-task.html', {
        'form': form,
    })


def add_project(request):
    form = NewProjectForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/pomodoro/new-task')
    else:
        pass
    return render(request, 'pomodoro/new-project.html', {
        'form': form,
    })


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    session_set = task.session_set.all()
    completed_sessions_count = session_set.filter(interrupted=False).count()
    interrupted_sessions_count = session_set.filter(interrupted=True).count()
    average_time = task.duration / session_set.count()

    return render(request, 'pomodoro/task-detail.html', {
        'sessions': session_set,
        'task': task,
        'completed_sessions_count': completed_sessions_count,
        'interrupted_sessions_count': interrupted_sessions_count,
        'average_time': average_time
    })


class EditSessionView(UpdateView):
    form_class = EditSessionForm
    model = Session
    template_name = 'pomodoro/edit-session.html'
    pk_url_kwarg = 'session_pk'


class EditTaskView(UpdateView):
    form_class = EditTaskForm
    model = Task
    template_name = 'pomodoro/task-edit.html'


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    sessions = Session.objects.filter(task__project__id=pk)
    stats = get_sessions_stats(sessions)
    return render(request, 'pomodoro/project-detail.html', {
        'project': project,
        'stats': stats,
    })


def start(request):
    try:
        task = Task.objects.get(id=request.POST['taskid'])
        session = Session.objects.create(task=task)
        start_time = timezone.now()
        session.start_time = start_time
        task.last_activity = start_time
        task.save()
        session.save()
        return render(request,
                      'pomodoro/start.html',
                      {'task': task,
                       'timeout_work': TIMEOUT_WORK,
                       })
    except Exception as e:
        raise e


def finish(request):

    if request.method == 'POST':
        try:
            task = Task.objects.get(id=request.POST['taskid'])
            last_session = task.session_set.first()
            finish_time = timezone.now()
            last_session.finish_time = finish_time
            delta = finish_time - last_session.start_time
            task.last_activity = finish_time
            task.save()

            if delta.seconds // 60 >= 25:
                last_session.interrupted = False
            last_session.save()
            return render(request,
                          'pomodoro/finish.html',
                          {'task': task,
                           'passed_time': delta.seconds,
                           })
        except Exception as e:
            raise e
    messages.success(request, 'The task finished with success.')
    return redirect('/pomodoro/home')


def all_tasks(request):
    tasks = Task.objects.all()
    task_count = tasks.count()
    session_count = 0
    total_duration = 0
    continued_count = 0
    interrupted_count = 0
    for task in tasks:
        session_count += task.session_set.count()
        total_duration += task.duration
        for session in task.session_set.all():
            if session.interrupted:
                interrupted_count += 1
            else:
                continued_count += 1

    paginator = Paginator(tasks, 25)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'pomodoro/all-tasks.html', {
        'tasks': tasks,
        'task_count': task_count,
        'session_count': session_count,
        'total_duration': total_duration,
        'average_duration': total_duration / session_count,
        'continued_count': continued_count,
        'interrupted_count': interrupted_count,
        'project_count': Project.objects.all().count(),
        'paginator': paginator,
        })


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('/pomodoro/home/')
    return render(request, 'pomodoro/delete-object.html', {
        'object': task,
        'type': 'task',
    })


def delete_history(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if request.method == 'POST':
        session.delete()
        return HttpResponseRedirect(session.task.get_absolute_url())

    return render(request, 'pomodoro/delete-object.html', {
        'object': session,
        'type:': 'history',
    })


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('/pomodoro/home')

    return render(request, 'pomodoro/delete-object.html', {
        'object': project,
        'type': 'project',
    })


def period_stats(request, period):
    if period in ['today', 'yesterday']:
        return day_period_stats(request, period)
    elif period == 'last-week':
        return last_week_stats(request)
    elif period == 'last-month':
        return last_month_stats(request)
    elif period == 'last-year':
        return last_year_stats(request)
    else:
        raise Http404


def day_period_stats(request, period):
    day = timezone.now() if period == 'today' else timezone.now().date() - timedelta(1)
    result = get_tasks_info_of_day(day)
    return render(request, 'pomodoro/day-stats.html', {
        'period': period,
        'date': day,
        'result': result,
    })


def last_week_stats(request):
    week_days = get_last_week_days()
    tasks_info = get_tasks_info_of_days(week_days)

    result = get_result_stats(tasks_info)
    result['start_week'] = week_days[0]
    result['end_week'] = week_days[6]

    return render(request, 'pomodoro/week-stats.html', {'result': result})


def last_month_stats(request):
    month_days = get_last_month_days_until_today()
    month_days.sort(reverse=True)

    tasks_info = get_tasks_info_of_days(month_days)

    result = get_result_stats(tasks_info)
    result['date'] = datetime.date.today()

    return render(request, 'pomodoro/month-stats.html', {'result': result})


def last_year_stats(request):
    stats = get_last_year_stats()
    return render(request, 'pomodoro/last-year-stats.html', {'stats': stats})


def get_project_tasks(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'pomodoro/project-tasks.html', {
        'project': project,
    })
