from django.urls import path, include
from .views import HomeVacanciesList, VacanciesByCity,vacancies_search


urlpatterns = [
    path('', HomeVacanciesList.as_view(), name='home'),
    path('city/<int:city_id>/', VacanciesByCity.as_view(), name='city'),
    path('search/', vacancies_search, name='search')
]