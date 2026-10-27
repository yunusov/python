from django.contrib import admin

from .models import Comment, Post, BlogUser

admin.site.register(Post)
admin.site.register(BlogUser)
admin.site.register(Comment)
