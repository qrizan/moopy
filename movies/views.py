from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre
from .forms import GenreForm, MovieForm


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
    return render(request, "movie/movie_list.html", context)


def movie_detail(request, movie_id =None):
    movie = get_object_or_404(Movie, id=movie_id)
    context = {
        "movie" : movie,
        "title" : movie.title
    }
    return render(request, "movie/movie_detail.html", context)


def movie_create(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        movie = form.save(commit=False)
        movie.save()
    # if request.method  == "POST":
    #     name = request.POST.get("name")
    #     Genre.objects.create(name=name)
        # success message
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(movie.get_absolute_url())
    else:
        messages.error(request, "Unsuccessfully Created")
    context = {
        "form" : form,
        "title" : "Create New Movie"
    }
    return render(request, "movie/movie_form.html", context)


def movie_update(request, movie_id = None):
    movie = get_object_or_404(Movie, id=movie_id)
    form = MovieForm(request.POST or None, request.FILES or None, instance= movie)
    if form.is_valid():
        movie = form.save(commit= False)
        movie.save()
        # success message
        messages.success(request, "Successfully updated")
        return HttpResponseRedirect(movie.get_absolute_url())

    context = {
        "title" : movie.title,
        "movie": movie,
        "form": form
    }
    return render(request, "movie/movie_form.html", context)


def movie_delete(request):
    pass


def genre_list(request):
    genres = Genre.objects.all()

    paginator = Paginator(genres, 5) # Show 10 genres per page

    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        all_genres = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_genres = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_genres = paginator.page(paginator.num_pages)

    context = {
        "all_genres" : all_genres,
        "title": "genre List",
        "page_request_var": page_request_var
    }

    # if request.user.is_authenticated():
    #     context = {
    #         "title": "List admin"
    #     }
    # else:
    #     context = {
    #         "title" : "movie List"
    #     }
    return render(request, "genre/genre_list.html", context)


def genre_detail(request, genre_id=None):
    genre = get_object_or_404(Genre, id=genre_id)
    context = {
        "genre" : genre,
        "title" : genre.name
    }
    return render(request, "genre/genre_detail.html", context)


def genre_create(request):
    form = GenreForm(request.POST or None)
    if form.is_valid():
        genre = form.save(commit=False)
        genre.save()
    # if request.method  == "POST":
    #     name = request.POST.get("name")
    #     Genre.objects.create(name=name)
        # success message
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(genre.get_absolute_url())
    else:
        messages.error(request, "Unsuccessfully Created")
    context = {
        "form" : form,
        "title" : "Create New Genre"
    }
    return render(request, "genre/genre_form.html", context)


def genre_update(request, genre_id = None):
    genre = get_object_or_404(Genre, id=genre_id)
    form = GenreForm(request.POST or None, instance= genre)
    if form.is_valid():
        genre = form.save(commit= False)
        genre.save()
        # success message
        messages.success(request, "Successfully updated")
        return HttpResponseRedirect(genre.get_absolute_url())

    context = {
        "title" : genre.name,
        "genre": genre,
        "form": form
    }
    return render(request, "genre/genre_form.html", context)


def genre_delete(request, genre_id=None ):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    messages.success(request, "Successfully deleted")
    return redirect("movies:genre_list")

