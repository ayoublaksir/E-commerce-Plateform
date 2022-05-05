from django import forms
from django.forms import ModelForm
from product.models import Comment, favorite


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['titre']
