from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class' : 'title',
                'placeholder' : '제목 입력...'
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class' : 'content',
                'placeholder' : '내용 입력...',
                'rows' : 5,
                'cols' : 30
            }
        )
    )
    weight = forms.FloatField(
        label='몸무게',
        widget=forms.TextInput(
            attrs={
                'class' : 'weight',
                'placeholder' : '입력...'
            }
        )
    )
    class Meta:
        model = Article
        fields = ('title', 'content',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='내용',
        widget=forms.TextInput(
            attrs={
                'class' : 'content',
                'placeholder' : '내용 입력...'
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content',)
