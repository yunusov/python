from django import forms

from blog_app.models import Post, BlogUser


class PostForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=BlogUser.objects.all(),
        label="Автор",
        empty_label="Выберите автора",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Post
        fields = ("name", "content", "user")
        labels = {
            "name": "Название поста",
            "content": "Содержимое поста",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание",
                    "rows": "5",
                }
            ),
            "user": forms.Select(attrs={"class": "form-control"}),
        }
