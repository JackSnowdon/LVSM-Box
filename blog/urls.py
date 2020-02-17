from django.urls import path
from .views import *

urlpatterns = [
    path("blog_home/", blog_home, name="blog_home"),
    path("add_post/", add_post, name="add_post"),
    path(r'edit_post/<int:pk>', edit_post, name="edit_post"),
    path(r'view_post/<int:pk>', view_post, name="view_post"),
    path(r'delete_post/<int:pk>', delete_post, name="delete_post"),
]