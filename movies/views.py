from django.shortcuts import render, get_object_or_404
from .models import Movie, Genre
from .forms import GenreForm


def movie_list(request):
    all_movies = Movie.objects.all()
    context = {
        "all_movies" : all_movies,
        "title": "movie List"
    }

    # if request.user.is_authenticated():
    #     context = {
    #         "title": "List admin"
    #     }
    # else:
    #     context = {
    #         "title" : "movie List"
    #     }
    return render(request, "movie_list.html", context)


def movie_detail(request):
    pass


def movie_create(request):
    pass


def movie_update(request):
    pass


def movie_delete(request):
    pass


def genre_list(request):
    all_genres = Genre.objects.all()
    context = {
        "all_genres" : all_genres,
        "title": "genre List"
    }

    # if request.user.is_authenticated():
    #     context = {
    #         "title": "List admin"
    #     }
    # else:
    #     context = {
    #         "title" : "movie List"
    #     }
    return render(request, "genre_list.html", context)


def genre_detail(request, genre_id=None):
    genre = get_object_or_404(Genre, id=genre_id)
    context = {
        "genre" : genre,
        "title" : genre.name
    }
    return render(request, "genre_detail.html", context)


def genre_create(request):
    form = GenreForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    # if request.method  == "POST":
    #     name = request.POST.get("name")
    #     Genre.objects.create(name=name)
    context = {
        "form" : form,
        "title" : "Create New Genre"
    }
    return render(request, "genre_create.html", context)


def genre_update(request):
    pass


def genre_delete(request):
    pass


