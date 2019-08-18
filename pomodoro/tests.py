from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from pomodoro.models import Task, TaskRun, ACTION_START, ACTION_FINISH
from pomodoro.views import home, new, start, finish, TIMEOUT_WORK

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        
    def test_new_task_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['taskname'] = 'A new task'
    
        response = new(request)
    
        self.assertEqual(Task.objects.count(), 1)
        first_task = Task.objects.first()
        self.assertEqual(first_task.name, 'A new task')
        
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['taskname'] = 'A new task'
    
        response = new(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        
    def test_home_page_displays_all_list_items(self):
        Task.objects.create(name='task 1')
        Task.objects.create(name='task 2')

        request = HttpRequest()
        response = home(request)

        self.assertIn('task 1', response.content.decode())
        self.assertIn('task 2', response.content.decode())
        
    def test_start_task_can_save_a_POST_request(self):
        task = Task.objects.create(name='test task')
        
        request = HttpRequest()
        request.method = 'POST'
        request.POST['taskid'] = task.id
    
        response = start(request)
    
        self.assertEqual(TaskRun.objects.count(), 1)
        first_task_run = TaskRun.objects.first()
        self.assertEqual(first_task_run.task, task)
        self.assertEqual(first_task_run.action, ACTION_START)
        
    def test_start_task_returns_correct_html(self):
        task = Task.objects.create(name='test task')
        
        request = HttpRequest()
        request.method = 'POST'
        request.POST['taskid'] = task.id
    
        response = start(request)
        
        expected_html = render_to_string('start.html',
                                         {'task':task,
                                          'timeout_work':TIMEOUT_WORK})
        self.assertEqual(response.content.decode(), expected_html)
        
    def test_finish_task_can_save_a_POST_request(self):
        task = Task.objects.create(name='test task')
        
        request = HttpRequest()
        request.method = 'POST'
        request.POST['taskid'] = task.id
    
        response = finish(request)
    
        self.assertEqual(TaskRun.objects.count(), 1)
        first_task_run = TaskRun.objects.first()
        self.assertEqual(first_task_run.task, task)
        self.assertEqual(first_task_run.action, ACTION_FINISH)
        
    def test_finish_task_returns_correct_html(self):
        task = Task.objects.create(name='test task')
        
        request = HttpRequest()
        request.method = 'POST'
        request.POST['taskid'] = task.id
    
        response = finish(request)
        
        expected_html = render_to_string('finish.html',
                                         {'task':task})
        self.assertEqual(response.content.decode(), expected_html)


class TaskModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_task = Task()
        first_task.name = 'The first task'
        first_task.save()

        second_task = Task()
        second_task.name = 'Task the second'
        second_task.save()

        saved_tasks = Task.objects.all()
        self.assertEqual(saved_tasks.count(), 2)

        first_saved_task = saved_tasks[0]
        second_saved_task = saved_tasks[1]
        self.assertEqual(first_saved_task.name, 'The first task')
        self.assertEqual(second_saved_task.name, 'Task the second')


class HistoryTaskModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        
        task = Task.objects.create(name='test task')
        task_run = TaskRun.objects.create(task=task, action=ACTION_START)
        task_run = TaskRun.objects.create(task=task, action=ACTION_FINISH)
        task_run = TaskRun.objects.create(task=task, action=ACTION_START)
        
        saved_task_runs = TaskRun.objects.all()
        self.assertEqual(saved_task_runs.count(), 3)

        first_saved_task_run = saved_task_runs[0]
        second_saved_task_run = saved_task_runs[1]
        third_saved_task_run = saved_task_runs[2]
        self.assertEqual(first_saved_task_run.task, task)
        self.assertEqual(first_saved_task_run.action, ACTION_START)
        self.assertEqual(second_saved_task_run.task, task)
        self.assertEqual(second_saved_task_run.action, ACTION_FINISH)
        self.assertEqual(third_saved_task_run.task, task)
        self.assertEqual(third_saved_task_run.action, ACTION_START)
