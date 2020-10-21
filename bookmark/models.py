from django.db import models


class BookmarkManager(models.Manager):
    def all(self):
        return super(BookmarkManager, self).all().filter(archive=False)


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(blank=True)
    safe = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    # make safe delete later
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    objects = BookmarkManager()

    class Meta:
        ordering = ['-created_at', ]


class Category(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
