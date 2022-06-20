from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Vacancy, City

from django.views.generic import ListView

from .scraper import *


class HomeVacanciesList(ListView):
    model = Vacancy
    template_name = 'vacancies/home_page.html'
    context_object_name = 'vacancies'
    paginate_by = 5
    allow_empty = True

    def get_queryset(self):
        if self.request.session.get('vacancies'):
            return Vacancy.objects.filter(id__in=self.request.session['vacancies'])
        else:
            return Vacancy.objects.none()


class VacanciesByCity(ListView):
    model = Vacancy
    template_name = 'vacancies/home_page.html'
    context_object_name = 'vacancies'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):

        if self.request.session.get('vacancies'):
            return Vacancy.objects.filter(id__in=self.request.session['vacancies'], city__id=self.kwargs['city_id'])
        else:
            return Vacancy.objects.none()


def vacancies_search(request):
    search_str = request.GET.get('q')

    data = work_ua(f'https://www.work.ua/jobs-{search_str}/')

    bulk_list1 = list()
    bulk_list2 = list()

    request.session['vacancies'] = list()

    cities = list(set(vacancy['city'] for vacancy in data))
    for city in cities:
        c = City(name=city)
        if City.objects.get_or_none(name=c.name) is None and c.name not in bulk_list1:
            bulk_list1.append(c)

    City.objects.bulk_create(bulk_list1)

    for vacancy in data:
        v = Vacancy(href=vacancy['href'],
                    short=vacancy['short'],
                    title=vacancy['title'],
                    company=vacancy['company'],
                    city=City.objects.get(name=vacancy['city']))

        if Vacancy.objects.get_or_none(href=v.href) is None and v.href not in bulk_list2:
            bulk_list2.append(v)
        else:
            request.session['vacancies'].append(Vacancy.objects.get_or_none(href=v.href).id)

    vacancies = Vacancy.objects.bulk_create(bulk_list2)

    if len(vacancies):
        for item in vacancies:
            request.session['vacancies'].append(item.id)

    return redirect('home')
