from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .models import Comment


def comment_thread(request, id):
    # comment = get_object_or_404(Comment, id=id)
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404
    # content_object = comment.content_object
    # content_id = comment.content_object.id

    initial_data = {
        "content_type": comment.content_type,
        "object_id": comment.object_id
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    # print(dir(form))
    # print(form.errors)

    if form.is_valid() and request.user.is_authenticated():
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

    context = {
        "comment" : comment,
        "comment_form" : form
    }
    return render(request, "comment/comment_thread.html", context)


@login_required
def comment_delete(request, id):
    # comment = get_object_or_404(Comment, id=id)
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if comment.user != request.user:
        # messages.success(request, "You don't have permission to view this")
        # raise Http404
        response = HttpResponse("You don't have permission to view this")
        response.status_code = 403
        return response

    if request.method == "POST":
        parent_comment_url = comment.content_object.get_absolute_url()
        comment.delete()
        messages.success(request, "This has ben deleted.")
        return HttpResponseRedirect(parent_comment_url)
    context = {
        "comment" : comment
    }
    return render(request, "comment/confirm_delete.html", context)