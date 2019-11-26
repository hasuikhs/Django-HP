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
                'placeholder' : '몸무게를 입력해주세요.'
            }
        )
    )
    height = forms.FloatField(
        label='신장',
        widget=forms.TextInput(
            attrs={
                'class' : 'height',
                'placeholder' : '키를 입력해주세요.'
            }
        )
    )
    image = forms.ImageField(
        label='니몸사진',
        widget=forms.FileInput(
            attrs={
                'class' : 'image',
            }
        )
    )
    secret = forms.IntegerField(
        label='비공개를 희망하시면 1이외의 값을 입력하여 주세요.',
        widget=forms.TextInput(
          attrs={
            'class' : 'secret'
          }
        )
            
    )
    
    
    class Meta:
      model = Article
      fields = ('title', 'content', 'weight', 'height', 'image',)


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
