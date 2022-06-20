from django.db import models
from django.conf import settings
from vacancies.models import Vacancy


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Vacancy, related_name='favorites', blank=True)
