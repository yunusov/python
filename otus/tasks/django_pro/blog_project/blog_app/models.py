from django.db import models


class EntityBase(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BlogUser(EntityBase):
    class Meta:
        db_table = "blog_app_user"


class Post(EntityBase):
    content = models.TextField()
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name="posts")


class Comment(EntityBase):
    content = models.TextField()
    name = None
    user = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
