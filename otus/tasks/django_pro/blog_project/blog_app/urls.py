from django.urls import path

from blog_app.views import (
    CommentDeleteView,
    CommentEditView,
    CommentView,
    IndexView,
    PostAddView,
    PostDeleteView,
    PostEditView,
    PostView,
    health_check,
)

app_name = "blog_app"

urlpatterns = [
    path("health/", health_check, name="health_check"),
    
    path("", IndexView.as_view(), name="index"),
    path("post/add/", PostAddView.as_view(), name="post_add"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<int:pk>/", PostView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", PostEditView.as_view(), name="post_edit"),
    path("comment/create/", CommentView.as_view(), name="comment_create"),
    path(
        "comment/<int:pk>/edit-inline/", CommentEditView.as_view(), name="comment_edit"
    ),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
]
