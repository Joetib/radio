from django import forms
from .models import Article, Comment, News, Podcast


class CreatePodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ("title", "series", "category", "picture", "audio", "body")

class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ("title", "category", "picture", "body")



class CommentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control mb-30", "placeholder": "Name",
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control mb-30", "placeholder": "Email",})
    )
    comment = forms.Field(widget=forms.Textarea(attrs={
        "class": "form-control mb-30",
        "placeholder": "Comment",
    }))

    class Meta:
        model = Comment
        fields = ( "name", "email", "comment")

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "series", "category", "picture", "body")

