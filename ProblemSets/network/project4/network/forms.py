from django import forms
from django.forms import ModelForm
from .models import NewPost

class NewPostForm(ModelForm):
    class Meta:
        model = NewPost
        fields=['newPost']
        labels={'newPost': 'New Post'}
        widgets={'newPost':forms.TextInput(attrs={'style':'width:50%;'})}



class PostForm(ModelForm):
    class Meta:
        model = NewPost
        fields=['user','postDate','likes','newPost']
        labels={'likes': 'likes'}
        widgets={'newPost':forms.TextInput(attrs={'readonly':'True'})}