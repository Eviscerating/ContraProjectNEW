from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from .forms import ArticleForm
from common.django_utils import arender
from common.auth import awriter_required
from .models import Article

@awriter_required
async def dashboard(request: HttpRequest) -> HttpResponse:
            return await arender(request, 'writer/dashboard.html')
        
@awriter_required
async def create_article(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if await form.ais_valid():
            article = await form.asave(commit = False)
            article.user = await aget_user(request)
            await article.asave()
            return redirect('my-articles')
    else:
        form = ArticleForm()
        
    context = {'create_article_form': form}            
    return await arender(request, 'writer/create-article.html', context)


@awriter_required
async def my_articles(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    articles = Article.objects.filter(user=user)
    context = {'my_articles': articles}
    return await arender(request, 'writer/my-articles.html', context)
