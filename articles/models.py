from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

CHOICES = (
    (1, "비공개"),
    (0, "공개"),    
)


# Create your models here.
class Hashtag(models.Model):
    content = models.TextField(unique=True)

    def __str__(self):
        return self.content
    

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    height = models.FloatField(blank=True,null=True)    
    weight = models.FloatField(blank=True,null=True)
    image = models.ImageField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles', blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    yes_no_required = models.NullBooleanField(choices = CHOICES)
    # 객체 표시 형식 수정
    def __str__(self):
        return f'[{self.pk}] {self.title}'

class Comment(models.Model):
    # Comment -> 이중 1:N 관계 (Article, User)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Model Loevel에서 메타데이터 옵션 설정 -> 정렬 기능 사용
    class Meta:
        ordering=['-pk',]

    # 객체 표현 방식
    def __str__(self):
        return self.content
    