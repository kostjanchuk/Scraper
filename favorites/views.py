from django.shortcuts import render, redirect
from django.views.generic import ListView
from vacancies.models import Vacancy
from account.models import Profile


class FavoritesList(ListView):
    model = Vacancy
    template_name = 'favorites/favorites-list.html'
    context_object_name = 'vacancies'
    allow_empty = True
    paginate_by = 5

    def get_queryset(self):
        if self.request.session.get('_auth_user_id'):
            if not self.request.session.get('favorites'):
                profile = Profile.objects.get(user__id=self.request.session['_auth_user_id'])
                self.request.session['favorites'] = [item.id for item in list(profile.favorites.all())]
            return Vacancy.objects.filter(id__in=self.request.session['favorites'])

        elif self.request.session.get('favorites'):
            return Vacancy.objects.filter(id__in=self.request.session['favorites'])
        else:
            return Vacancy.objects.none()


def add_to_favorites(request, id):
    previous_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        if request.session.get('_auth_user_id'):
            if not request.session.get('favorites'):
                profile = Profile.objects.get(user__id=request.session['_auth_user_id'])
                lst = list(profile.favorites.all())
                request.session['favorites'] = [item.id for item in lst]

        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        item_exist = next((item for item in request.session['favorites'] if item == int(id)), False)

        if not item_exist:
            request.session['favorites'].append(int(id))
            request.session.modified = True

        if request.session.get('_auth_user_id'):
            vacancy=Vacancy.objects.get(id=int(id))
            profile = Profile.objects.get(user__id=request.session['_auth_user_id'])
            profile.favorites.add(vacancy)
    return redirect(previous_url)


def remove_from_favorites(request, id):
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item == int(id) :
                request.session['favorites'].remove(item)

        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True

    if request.session.get('_auth_user_id'):
        vacancy = Vacancy.objects.get(id=int(id))
        profile = Profile.objects.get(user__id=request.session['_auth_user_id'])
        profile.favorites.remove(vacancy)

        if not request.session['favorites']:
            del request.session['favorites']

    return redirect(previous_url)


def delete_favorites(request):
    previous_url = request.META.get('HTTP_REFERER')
    if request.session.get('_auth_user_id'):
        profile = Profile.objects.get(user__id=request.session['_auth_user_id'])
        profile.favorites.clear()
    if request.session.get('favorites'):
        del request.session['favorites']
    return redirect(previous_url)
