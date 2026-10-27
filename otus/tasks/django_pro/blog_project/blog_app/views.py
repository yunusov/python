from blog_project.loguru_config import AppLogger
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import PostForm
from .models import BlogUser, Comment, Post

logger = AppLogger().get_logger()

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok", "database": "connected", "timestamp": timezone.now()})
    except Exception as exc:
        return JsonResponse({"status": "error", "database": str(exc), "timestamp": timezone.now()}, status=500)


class IndexView(ListView):
    model = Post
    select_related = ("user",)
    template_name = "index.html"
    context_object_name = "posts"
    paginate_by = 10
    ordering = ["-created_at"]


class PostView(DetailView):
    """Просмотр поста"""

    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["comments"] = self.object.post_comments.order_by("created_at")
        return context


class PostAddView(CreateView):
    """Добавление поста."""

    model = Post
    template_name = "post.html"
    form_class = PostForm
    success_url = reverse_lazy("blog_app:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать пост"
        return context


class PostEditView(UpdateView):
    """Редактирование поста."""

    model = Post
    template_name = "post.html"
    form_class = PostForm
    success_url = reverse_lazy("blog_app:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Редактировать пост "' + self.object.name + '"'
        return context


class PostDeleteView(View):
    """Удаление поста."""

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        post.delete()
        return redirect("blog_app:index")


class CommentView(View):
    """Добавление комментария."""

    model = Comment

    def post(self, request, *args, **kwargs):
        logger.info(f"{request.user}")
        id = request.POST.get("post_id")
        content = request.POST.get("content")
        user = BlogUser.objects.order_by("?").first()
        if not id or not content or not user:
            return redirect("blog_app:index")
        post = get_object_or_404(Post, pk=id)
        obj = self.model.objects.create(
            post=post,
            content=content,
            user=user,
        )
        return redirect("blog_app:post_detail", pk=id)


class CommentEditView(View):
    """Изменение комментария."""

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        content = request.POST.get("content")
        if content:
            comment.content = content
            comment.save()
        return redirect("blog_app:post_detail", pk=comment.post_id)


class CommentDeleteView(View):
    """Удаление комментария."""

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        post_id = comment.post_id
        comment.delete()
        return redirect("blog_app:post_detail", pk=post_id)
