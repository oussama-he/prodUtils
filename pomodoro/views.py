from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.template.loader import get_template
from django.http import HttpResponse

from pomodoro.models import Task, Session, Project
from .forms import NewTaskForm, NewProjectForm
from .utils import calculate_duration, get_tasks_duration, get_task_sessions
from weasyprint import HTML, CSS
from datetime import timedelta
TIMEOUT_WORK = 25
# TODO: Add the ability to import tasks from todo app


def get_all_projects(request):

    projects = Project.objects.all()
    return render(request, 'pomodoro/all-tasks.html', {
        "projects": projects,
})


def home(request):
    # later make these in model manager or something else

    def get_total_duration(task_duration):
        total_duration = 0
        for value in task_duration.values():
            total_duration += value
        return total_duration

    today_sessions = Session.objects.filter(start_time__date=timezone.now().date())
    today_task_sessions = get_task_sessions(today_sessions)
    today_task_duration = get_tasks_duration(today_task_sessions)
    today_total_duration = get_total_duration(today_task_duration)

    yesterday_sessions = Session.objects.filter(finish_time__date=timezone.now().date()-timedelta(1))
    yesterday_task_sessions = get_task_sessions(yesterday_sessions)
    yesterday_task_duration = get_tasks_duration(yesterday_task_sessions)
    yesterday_total_duration = get_total_duration(yesterday_task_duration)

    date = timezone.now().date()
    start_week = date - timedelta(date.weekday())
    end_week = start_week + timedelta(7)
    last_week_sessions = Session.objects.filter(finish_time__range=[start_week, end_week])
    last_week_task_sessions = get_task_sessions(last_week_sessions)
    last_week_task_duration = get_tasks_duration(last_week_task_sessions)
    last_week_total_duration = get_total_duration(last_week_task_duration)
    
    last_month_sessions = Session.objects.filter(finish_time__month=timezone.now().month,
                                                  finish_time__year=timezone.now().year)
    last_month_task_sessions = get_task_sessions(last_month_sessions)
    last_month_task_duration = get_tasks_duration(last_month_task_sessions)
    last_month_total_duration = get_total_duration(last_month_task_duration)

    tasks = Task.objects.all()[:7]
    return render(request, 'pomodoro/home.html',
                  # {'tasks': tasks,
                  #  'today_tasks': today_tasks,
                  #  'today_duration': today_duration,
                  #  'yesterday_tasks': yesterday_tasks,
                  #  ''
                  #  'last_week_tasks': last_week_tasks,
                  #  'last_month_tasks': last_month_tasks,
                  #  }
                  locals()
                  )


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
# def new(request):
#     if request.method == 'POST':
#         try:
#             Task.objects.create(name=request.POST['taskname'])
#         except:
#             pass
#     return redirect('/pomodoro/home')


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    session_set = task.session_set.all()

    return render(request, 'pomodoro/task-detail.html', {
        'histories': session_set,
        'task': task,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    return render(request, 'pomodoro/project-detail.html', {
        'project': project,
    })


def start(request):
    print('from start def before try block')
    try:
        print('from start view:', request.POST['taskid'])
        task = Task.objects.get(id=request.POST['taskid'])
        session = Session.objects.create(task=task)
        session.start_time = timezone.now()
        session.save()
        return render(request,
                      'pomodoro/start.html',
                      {'task': task,
                       'timeout_work': TIMEOUT_WORK,
                       })
    except Exception as e:
        raise e
    return redirect('/pomodoro/home')


def finish(request):

    if request.method == 'POST':
        try:
            task = Task.objects.get(id=request.POST['taskid'])
            last_session = task.session_set.last()
            last_session.finish_time = timezone.now()
            delta = last_session.finish_time - last_session.start_time
            # to change the value of finish_time field in task model
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


def session(request):
    # todo: add pagination
    tasks = Task.objects.all()
    return render(request, 'pomodoro/history.html', {'tasks': tasks})


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
# todo: use messages framework to show a message after finishing the timer
# todo: change notifications to webPush js framework

from . import utils
import os
def generate_pdf(request):
    html_template = get_template('pomodoro/dirs.html')
    user = request.user
    base_dir = "/home/oussama/Desktop/الفلاش_الدعوي"
    result = os.scandir(base_dir)
    result = utils.list_files_name(base_dir, result, sep='')
    print(result)
    rendered_html = html_template.render({'request': request, 'you': user, 'result': result}).encode(encoding="UTF-8")

    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(string="""
    @page {
    size: a4 portrait;
    margin: 0mm 0mm 0mm 0mm;
    counter-increment: page;
    /*@bottom-center {
        content: '(c) XX COMPANY - Page ' counter(page);
        white-space: pre;
        color: grey;
    }*/
    }
    body {
        background-color: #263238;
        font-family: 'Droid arabic naskh';
    }
    .dir {
        /*color: #f0685a;*/
        color: #FF5370;
        margin-right: 15px;
        font-size: 25px;
    }
    .file {
        color: #C3CEE3;
        margin-right: 40px;
        font-size: 15px;
        line-height: 50%;
    }
    h1 {
        color: blue;
    }
    """)])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return http_response


def get_tasks(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = project.task_set.all()
    return render(request, 'pomodoro/tasks.html', {
        'tasks': tasks,
    })
