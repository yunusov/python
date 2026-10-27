from django.test import TestCase
from django.urls import reverse
from blog_app.models import BlogUser, Post, Comment


class BlogUserModelTest(TestCase):
    """Тесты модели BlogUser."""

    def test_create_blog_user(self):
        """Создание пользователя с валидными данными."""
        user = BlogUser.objects.create(name="Test User")
        self.assertEqual(user.name, "Test User")
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_blog_user_str(self):
        """__str__ возвращает name."""
        user = BlogUser.objects.create(name="Display Name")
        self.assertEqual(str(user), "Display Name")


class PostModelTest(TestCase):
    """Тесты модели Post."""

    def setUp(self):
        self.user = BlogUser.objects.create(name="Author")

    def test_create_post(self):
        """Создание поста с валидными данными."""
        post = Post.objects.create(
            name="Post Title",
            content="Post body text",
            user=self.user,
        )
        self.assertEqual(post.name, "Post Title")
        self.assertEqual(post.content, "Post body text")
        self.assertEqual(post.user, self.user)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_post_str(self):
        """__str__ возвращает name поста."""
        post = Post.objects.create(
            name="My Post", content="Content", user=self.user
        )
        self.assertEqual(str(post), "My Post")

    def test_user_cascade_delete_posts(self):
        """Удаление пользователя удаляет его посты (CASCADE)."""
        Post.objects.create(name="P1", content="C1", user=self.user)
        Post.objects.create(name="P2", content="C2", user=self.user)
        self.assertEqual(Post.objects.count(), 2)
        self.user.delete()
        self.assertEqual(Post.objects.count(), 0)


class CommentModelTest(TestCase):
    """Тесты модели Comment."""

    def setUp(self):
        self.user = BlogUser.objects.create(name="Commenter")
        self.post = Post.objects.create(
            name="Post", content="Body", user=self.user
        )

    def test_create_comment(self):
        """Создание комментария с валидными данными."""
        comment = Comment.objects.create(
            content="Nice post!",
            user=self.user,
            post=self.post,
        )
        self.assertEqual(comment.content, "Nice post!")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)

    def test_comment_user_cascade_delete(self):
        """Удаление автора удаляет его комментарии (CASCADE)."""
        Comment.objects.create(content="C1", user=self.user, post=self.post)
        Comment.objects.create(content="C2", user=self.user, post=self.post)
        self.assertEqual(Comment.objects.count(), 2)
        self.user.delete()
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_post_cascade_delete(self):
        """Удаление поста удаляет его комментарии (CASCADE)."""
        Comment.objects.create(content="C1", user=self.user, post=self.post)
        Comment.objects.create(content="C2", user=self.user, post=self.post)
        self.assertEqual(Comment.objects.count(), 2)
        self.post.delete()
        self.assertEqual(Comment.objects.count(), 0)

    def test_entity_base_timestamps(self):
        """created_at и updated_at устанавливаются автоматически."""
        comment = Comment.objects.create(
            content="Timestamp test",
            user=self.user,
            post=self.post,
        )
        # created_at установлен при создании
        self.assertIsNotNone(comment.created_at)
        original_created = comment.created_at

        # Имитация обновления
        comment.content = "Updated content"
        comment.save()
        comment.refresh_from_db()
        # updated_at изменился
        self.assertGreater(comment.updated_at, original_created)


class IndexViewTest(TestCase):
    """Тесты IndexView — список постов с пагинацией."""

    @classmethod
    def setUpTestData(cls):
        user = BlogUser.objects.create(name="Author")
        cls.posts = [
            Post.objects.create(
                name=f"Post {i}", content=f"Content {i}", user=user
            )
            for i in range(15)
        ]

    def test_index_view_status_code(self):
        """GET / возвращает 200."""
        response = self.client.get(reverse("blog_app:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        """В контексте есть posts и page_obj."""
        response = self.client.get(reverse("blog_app:index"))
        self.assertIn("posts", response.context)
        self.assertIn("page_obj", response.context)
        self.assertTrue(response.context["is_paginated"])

    def test_index_view_ordering(self):
        """Посты отсортированы по убыванию created_at."""
        response = self.client.get(reverse("blog_app:index"))
        posts = list(response.context["page_obj"])
        for i in range(len(posts) - 1):
            self.assertGreaterEqual(
                posts[i].created_at, posts[i + 1].created_at
            )

    def test_index_view_pagination(self):
        """Пагинация: 10 постов на страницу, 15 постов = 2 страницы."""
        # Первая страница — 10 постов
        response = self.client.get(reverse("blog_app:index"), {"page": 1})
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertTrue(response.context["is_paginated"])

        # Вторая страница — 5 постов
        response = self.client.get(reverse("blog_app:index"), {"page": 2})
        self.assertEqual(len(response.context["page_obj"]), 5)

    def test_index_view_page_404(self):
        """Недоступная страница пагинации возвращает 404."""
        response = self.client.get(reverse("blog_app:index"), {"page": 99})
        self.assertEqual(response.status_code, 404)
