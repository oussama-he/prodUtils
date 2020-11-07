from django.urls import reverse
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    # tags = models.ManyToManyField('tags')

    @property
    def duration(self) -> int:
        total_duration = 0
        for session in self.session_set.all():
            # perhaps we can add a structure or something else tha have meaning to distinguish the error
            if not session.finish_time:
                continue

            total_duration += session.duration
        return total_duration

    def get_absolute_url(self):
        return reverse("pomodoro:task-detail", kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-last_activity']

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100)
    # todo: change the name to created at
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_activity = models.DateTimeField(auto_now_add=False, auto_now=True)

    def get_absolute_url(self):
        return reverse("pomodoro:project-detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    @property
    def task_count(self):
        return self.task_set.count()

    def passed_time(self):
        task_set = self.task_set.all()
        duration = 0
        for task in task_set:
            duration += task.duration
        return duration

    class Meta:
        ordering = ['-last_activity']


class Session(models.Model):
    task = models.ForeignKey('Task', blank=True, null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-start_time']

    @property
    def duration(self) -> int:
        if self.finish_time is not None:
            delta = self.finish_time - self.start_time
            return int(delta.total_seconds())
        return 0

    @property
    def interrupted(self):
        """
        Checks if the session is 25 minutes or more
        :rtype: bool
        """
        if self.duration >= 25*60:
            return False
        return True

    def get_absolute_url(self):
        return reverse("pomodoro:task-detail", kwargs={'pk': self.task.pk})
    
    def __str__(self):
        return self.task.title


