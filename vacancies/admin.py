from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Vacancy,City


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'href', 'short', 'city', 'company', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title', 'city', 'company')
    # list_editable = ('created_at',)
    list_filter = ('created_at', 'city','company')
    fields = ('title', 'href', 'short', 'city', 'company', 'created_at',)
    # readonly_fields = ('title', 'href','short', 'city','company', 'created_at',)
    save_on_top = True


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)



# admin.site.site_title = 'Управление новостями'
# admin.site.site_header = 'Управление новостями'

