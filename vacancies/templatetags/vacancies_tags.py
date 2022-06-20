from django import template

from vacancies.models import City, Vacancy
from django.db.models import *
from account.models import Profile
register = template.Library()


@register.inclusion_tag('vacancies/list_cities.html', takes_context=True)
def show_cities(context):
    cities = City.objects.filter(vacancy__in=context['request'].session['vacancies']).distinct().annotate(
        cnt=Count('vacancy')).filter(cnt__gt=0)

    return {'cities':cities}
