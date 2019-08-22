from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=55)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_total_cost(self):
        expenses = self.expense_set.all()
        total = 0
        for expense in expenses:
            total += expense.cost
        return total

    def get_absolute_url(self):
        return reverse('budget:category-details', kwargs={'slug': slugify(self.title)})

    class Meta:
        verbose_name_plural = 'categories'


class Expense(models.Model):
    cost = models.IntegerField()
    timestamp = models.DateField(verbose_name='date')
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey('Category')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.cost, self.category.title)

    class Meta:
        ordering = ['-timestamp', ]

