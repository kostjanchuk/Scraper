from django.db import models
from django.urls import reverse


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class City(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('city', kwargs={"city_id": self.pk})

    def __str__(self):
        return self.name

    objects = GetOrNoneManager()


class Vacancy (models.Model):
    title = models.CharField(max_length=255, db_index=True,blank=True)
    href = models.TextField(blank=True, unique=True)
    short = models.TextField(blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, db_index=True)
    company = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('view_vacancies', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-created_at', '-added_at']

