from django.db import models


def upload_to(instance, filename):
    date = datetime.now()
    filename, extension = filename.rsplit(".", 1)
    filename = "%d-%d-%d-%d-%d-%d-%d.%s" % (date.year, date.month, date.day, date.hour,
                                            date.minute, date.second, date.microsecond, extension)
    if extension.lower() == "pdf":
        filename = os.path.join('pdf', filename)
    else:
        filename = os.path.join('avatars', filename)
    return filename

class Task(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.TimeField()
    date = models.DateTimeField()
    done = models.BooleanField(default=True)
    # we ommit this field
    passed = models.BooleanField(default=True)



class FileURL(models.Model):
    source = models.FileField(upload_to=upload_to, blank=True)