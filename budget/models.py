from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from utils.utils import generate_random_str


class Category(models.Model):
    title = models.CharField(max_length=55)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
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
        return reverse('budget:category-details', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'categories'


class Expense(models.Model):
    cost = models.IntegerField()
    timestamp = models.DateField(verbose_name='date', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey('Category')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.cost, self.category.title)

    class Meta:
        ordering = ['-timestamp', ]


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    queryset = Category.objects.filter(slug=slug).order_by('-pk')

    if queryset.exists():
        slug = "%s-%s" % (slug, generate_random_str())

    instance.slug = slug


pre_save.connect(pre_save_category_receiver, sender=Category)
