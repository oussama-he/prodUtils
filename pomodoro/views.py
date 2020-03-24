from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import UpdateView

from pomodoro.models import Task, Session, Project
from .forms import NewTaskForm, NewProjectForm, EditSessionForm, EditTaskForm
from weasyprint import HTML, CSS
from datetime import timedelta
TIMEOUT_WORK = 25
# TODO: Add the ability to import tasks from todo app


def get_all_projects(request):
    projects = Project.objects.all()
    return render(request, 'pomodoro/all-projects.html', {
        "projects": projects,
})


def home(request):
    # later make these in model manager or something else

    def get_total_duration(queryset):
        total_duration = 0
        for entry in queryset:
            total_duration += entry.get_duration()
        return total_duration

    def get_sessions_info(sessions):
        return (get_total_duration(sessions), sessions.count(),
        sessions.filter(interrupted=False).count(), sessions.filter(interrupted=True).count())
    
    today_sessions = Session.objects.filter(start_time__date=timezone.now().date())
    today_sessions_duration, today_sessions_count,\
    today_sessions_continued_count, today_sessions_interrupted_count = get_sessions_info(today_sessions)

    yesterday_sessions = Session.objects.filter(finish_time__date=timezone.now().date()-timedelta(1))
    yesterday_sessions_duration, yesterday_sessions_count,\
    yesterday_sessions_continued_count, yesterday_sessions_interrupted_count = get_sessions_info(yesterday_sessions)

    date = timezone.now().date()
    start_week = date - timedelta(date.weekday())
    end_week = start_week + timedelta(7)
    last_week_sessions = Session.objects.filter(finish_time__range=[start_week, end_week])
    last_week_sessions_duration, last_week_sessions_count,\
    last_week_sessions_continued_count, last_week_sessions_interrupted_count = get_sessions_info(last_week_sessions)

    last_month_sessions = Session.objects.filter(finish_time__month=timezone.now().month,
                                                  finish_time__year=timezone.now().year)
    last_month_sessions_duration, last_month_sessions_count,\
    last_month_sessions_continued_count, last_month_sessions_interrupted_count = get_sessions_info(last_month_sessions)

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
            last_session = task.session_set.first()
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


def all_tasks(request):
    # todo: add pagination
    tasks = Task.objects.all()
    return render(request, 'pomodoro/all-tasks.html', {'tasks': tasks})


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


def get_project_tasks(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'pomodoro/project-tasks.html', {
        'project': project,
    })
