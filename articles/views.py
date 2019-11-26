import hashlib
from IPython import embed
from itertools import chain
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    articles = Article.objects.all()[::-1]
    paginator = Paginator(articles, 8)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles' : articles}
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)        
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            height = form.cleaned_data.get('height')  
            weight = form.cleaned_data.get('weight')
            image = form.cleaned_data.get('image')
            yes_no_required = form.cleaned_data.get('yes_no_required')
            user_id = request.user.id
            article = Article.objects.create(title=title, content=content, height=height, weight=weight, image=image, yes_no_required=yes_no_required , user_id=user_id)            
            for word in article.content.split():
                if word.startswith('#'):
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)

        return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {'form':form}
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    
    article = get_object_or_404(Article, pk=article_pk)
    if article.yes_no_required == 1:
        if request.user.is_authenticated:
            if request.user == article.user:
                person = get_object_or_404(get_user_model(), pk=article.user_id)
                comment_form = CommentForm()
                comments = article.comment_set.all()
        
                context = {
                    'article' : article,
                    'comment_form' : comment_form,
                    'comments' : comments,
                    'person' : person,
                }
                return render(request, 'articles/detail.html', context)
        return redirect('articles:index')
    else:
        person = get_object_or_404(get_user_model(), pk=article.user_id)
        comment_form = CommentForm()
        comments = article.comment_set.all()
        
        context = {
            'article' : article,
            'comment_form' : comment_form,
            'comments' : comments,
            'person' : person,
        }
        return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
        else:
            return redirect('articles:detail', article.pk)
    return redirect('articles:index')

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article=form.save()

                # hashtag
                article.hashtags.clear()
                for word in article.content.split():
                    if word.startswith('#'):
                        hashtag = Hashtag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)

                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    
    context = {
        'form' : form,
        'article' : article,    
    }
    return render(request, 'articles/form.html', context)

@require_POST
def comments_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = article.user
            comment.save()
    return redirect('articles:detail', article.pk)
    

@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', article_pk)

@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    user = request.user

    if user in article.like_users.all():
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
        
    return redirect('articles:index')

@login_required
def follow(request, article_pk, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('articles:detail', article_pk)

# 내가 팔로우 하는 사람의 글 + 내가 작성한 글
def list(request):
    followings = request.user.followings.all()
    followings = chain(followings, [request.user])
    articles = Article.objects.filter(user__in=followings).order_by('-pk').all()
    comment_form = CommentForm()
    context = {
        'articles' : articles,
        'comment_form' : comment_form,
    }
    return render(request, 'articles/article_list.html', context)

def explore(request):
    articles = Article.objects.all()
    comment_form = CommentForm()
    context = {
        'articles' : articles,
        'comment_form' : comment_form,
    }
    return render(request, 'articles/article_list.html', context)

# Hashtag 글 모아보기
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    articles = hashtag.article_set.order_by('-pk')
    context = {
        'hashtag' : hashtag,
        'articles' : articles,
    }
    return render(request, 'articles/hashtag.html', context)