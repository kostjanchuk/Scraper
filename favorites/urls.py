from django.urls import path, include
from . import views

app_name = 'favorites'

urlpatterns = [
    path('favorites/', include([

        path('', views.FavoritesList.as_view(), name='favorites_list'),

        path('<id>/add/', views.add_to_favorites, name='add_to_favorites'),
        path('<id>/remove/', views.remove_from_favorites, name='remove_from_favorites'),
        path('delete/', views.delete_favorites, name='delete_favorites'),
    ]))
]