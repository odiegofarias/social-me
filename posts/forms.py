from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    conteudo = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'No que está pensando...',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Post
        exclude = ('autor', )