from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from .models import Subscription
from writer.models import Article

from common.django_utils import arender 
from common.auth import aclient_required

PlanChoices = Subscription.PlanChoices

@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    try:
        subscription = await Subscription.objects.aget(user=user, is_active=True)
        plan = PlanChoices(subscription.plan)
        susbscription_plan = plan.label
    except ObjectDoesNotExist:
        susbscription_plan = 'No subscription plan yet'
        
    context = {'subscription_plan': susbscription_plan}
    return await arender (request, 'client/dashboard.html', context)

@aclient_required
async def browse_articles(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    try:
        subscription = await Subscription.objects.aget(user=user, is_active=True)
        has_subscription = True
        plan = PlanChoices(subscription.plan)
        if plan == PlanChoices.STANDARD:
                articles = Article.objects.filter(is_premium=False)
        else:
                articles = Article.objects.all()
    except ObjectDoesNotExist: 
        has_subscription = False
        articles =[]
        
        
    context = {'has_subscription': has_subscription, 'articles': articles}
    return await arender(request, 'client/browse-articles.html', context)

