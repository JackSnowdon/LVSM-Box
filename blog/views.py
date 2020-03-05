from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .models import *
from .forms import *


def blog_home(request):
    posts = Post.objects.filter(content_level=1)
    return render(request, "blog_home.html", {"posts": posts})


@login_required
def content_2(request):
    if request.user.profile.staff_access:
        posts = Post.objects.filter(content_level=2)
        return render(request, "content_2.html", {"posts": posts})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("blog_home")


@login_required
def content_3(request):
    if request.user.profile.staff_access:
        user = User.objects.get(email=request.user.email)
        profile = user.profile
        posts = profile.posts.filter(content_level=3)
        return render(request, "content_3.html", {"posts": posts})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("blog_home")


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
    comments = this_post.post_comments.all()
    return render(request, "view_post.html", {"this_post": this_post, "comments": comments})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post           
            comment.created_date = datetime.now()
            user = request.user
            comment.author = user.profile
            comment.save()
            messages.error(
                request, "Added Comment", extra_tags="alert"
            )
            return redirect("blog_home")
    else:
        comment_form = CommentForm()
        return render(request, "add_comment.html", {"comment_form": comment_form, "post": post })