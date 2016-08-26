from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm
from django.utils import timezone
from comments.forms import CommentForm
from comments.models import Comment


def movie_list(request):
    today = timezone.now().date()
    movies = Movie.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        movies = Movie.objects.all()

    query = request.GET.get("q")
    if query:
        movies = movies.filter(title__icontains=query)

    paginator = Paginator(movies, 3)

    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        all_movies = paginator.page(page)
    except PageNotAnInteger:
        all_movies = paginator.page(1)
    except EmptyPage:
        all_movies = paginator.page(paginator.num_pages)

    context = {
        "all_movies" : all_movies,
        "title": "movie List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "movie/movie_list.html", context)


def movie_list_genre(request, genre_id= None):
    today = timezone.now().date()
    movies = Movie.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        movies = Movie.objects.all()

    movies = movies.filter(genre_id= genre_id)

    query = request.GET.get("q")
    if query:
        movies = movies.filter(title__icontains=query)

    paginator = Paginator(movies, 2)

    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        all_movies = paginator.page(page)
    except PageNotAnInteger:
        all_movies = paginator.page(1)
    except EmptyPage:
        all_movies = paginator.page(paginator.num_pages)

    context = {
        "all_movies" : all_movies,
        "title": "Movie List",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "movie/movie_list.html", context)


def movie_detail(request, slug= None):
    movie = get_object_or_404(Movie, slug=slug)

    initial_data = {
        "content_type" : movie.get_content_type,
        "object_id": movie.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get("object_id")
        message = form.cleaned_data.get("message")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1 :
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                user = request.user,
                content_type = content_type,
                object_id = object_id,
                message = message,
                parent_id = parent_id,
                parent = parent_obj
        )

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = movie.comments
    context = {
        "movie" : movie,
        "title" : movie.title,
        "comments" : comments,
        "comment_form" : form
    }
    return render(request, "movie/movie_detail.html", context)


def movie_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404

    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        movie = form.save(commit=False)
        movie.user = request.user
        movie.save()
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
    else:
        messages.error(request, "Unsuccessfully Updated")
    context = {
        "title" : movie.title,
        "movie": movie,
        "form": form
    }
    return render(request, "movie/movie_form.html", context)


def movie_delete(request, movie_id = None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404

    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    messages.success(request, "Successfully deleted")
    return redirect("movies:movie_list")
