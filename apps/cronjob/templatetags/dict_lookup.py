from django import template
from django.core.exceptions import ObjectDoesNotExist
import re
import django

django.setup()
register = template.Library()


@register.filter()
def dictKeyLookup(the_dict, key):
    # Try to fetch from the dict, and if it's not found return an empty string.
    #print the_dict
    return the_dict.get(key, '')


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='filter_tasks')
def filter_tasks(task_list):
    return [app for app in task_list if app.startswith('cronjob.')]
            # not app.startswith('celery.')
            # and not app.startswith('kubernode.')
            # and not app.startswith('workflow.')
            # and not app.startswith('autocronjob.celery.debug_task')]
