from django.db import models


class ToDoManger(models.Manager):
    pass


class Set(models.Model):
    title = models.CharField(max_length=55)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_used', ]


class ToDo(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    PRIORITY = (
        ('N', 'Normal'),
        ('M', 'Medium'),
        ('U', 'Urgent'),
    )
    priority = models.CharField(max_length=1, choices=PRIORITY)
    set = models.ForeignKey(to='Set', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp', ]