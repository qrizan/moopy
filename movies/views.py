from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre
from .forms import GenreForm, MovieForm
from django.utils import timezone


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


def movie_detail(request, slug= None):
    movie = get_object_or_404(Movie, slug=slug)
    context = {
        "movie" : movie,
        "title" : movie.title
    }
    return render(request, "movie/movie_detail.html", context)


def movie_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_autheticated():
        raise Http404

    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        movie = form.save(commit=False)
        movie.user = request.user
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404

    movie = get_object_or_404(Movie, id=movie_id)
    form = MovieForm(request.POST or None, request.FILES or None, instance= movie)
    if form.is_valid():
        movie = form.save(commit= False)
        movie.user = request.user
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


def movie_delete(request, movie_id = None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_autheticated():
        raise Http404

    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    messages.success(request, "Successfully deleted")
    return redirect("movies:movie_list")


def genre_list(request):
    today = timezone.now().date()
    genres = Genre.objects.active()
    if request.user.is_staff or request.user.is_superuser:
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
        "page_request_var": page_request_var,
        "today": today,
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


def genre_detail(request, slug= None):
    genre = get_object_or_404(Genre, slug=slug)
    if genre.publish > timezone.now().date() or genre.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {
        "genre" : genre,
        "title" : genre.name
    }
    return render(request, "genre/genre_detail.html", context)


def genre_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404

    form = GenreForm(request.POST or None)
    if form.is_valid():
        genre = form.save(commit=False)
        genre.user = request.user
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_autheticated():
        raise Http404

    genre = get_object_or_404(Genre, id=genre_id)
    form = GenreForm(request.POST or None, instance= genre)
    if form.is_valid():
        genre = form.save(commit= False)
        genre.user = request.user
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_autheticated():
        raise Http404

    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    messages.success(request, "Successfully deleted")
    return redirect("movies:genre_list")

