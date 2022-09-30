from django import forms
from .models import Post,Comment
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(): 
        model = User
        fields = ('username','email','password')



class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author','title','text')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'textinputclass'}),# this classes are css classes
            'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent '}) 
        }  # this is how you can affect the styling of your fields and  connects to the css classes

    

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields =('author','text')

        widgets = {
            'author' : forms.TextInput(attrs={'class':'textinputclass'}),
            'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea  '})
        }