from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Post
from .forms import PostForm


def blog_home(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, "blog_home.html", {"posts": posts})


@login_required
def add_post(request):
    if request.user.profile.staff_access:
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.created_on = datetime.now()
                post.last_modified = datetime.now()
                user = request.user
                post.done_by = user.profile
                post.save()
                messages.error(
                    request, "Added {0}".format(post.title), extra_tags="alert"
                )
                return redirect("blog_home")
        else:
            post_form = PostForm()
        return render(request, "add_post.html", {"post_form": post_form})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("blog_home")
        

@login_required
def edit_post(request, pk):
    if request.user.profile.staff_access:
        this_post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            post_form = PostForm(request.POST, instance=this_post)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.last_modified = datetime.now()
                post.save()
                messages.error(
                    request, "Edited {0} @ {1}".format(post.title, post.last_modified), extra_tags="alert"
                )
                return redirect("blog_home")
        else:
            post_form = PostForm(instance=this_post)
        return render(request, "edit_post.html", {"post_form": post_form, "this_post": this_post })
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("blog_home")


@login_required
def delete_post(request, pk):
    if request.user.profile.staff_access:
        instance = Post.objects.get(pk=pk)
        messages.error(request, "Deleted {0}".format(instance.title), extra_tags="alert")
        instance.delete()
        return redirect(reverse("blog_home"))
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("blog_home")


def view_post(request, pk):
    this_post = get_object_or_404(Post, pk=pk)
    this_post.views += 1
    this_post.save()
    return render(request, "view_post.html", {"this_post": this_post})

