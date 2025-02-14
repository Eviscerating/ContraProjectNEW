from functools import wraps 

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from common.django_utils import AsyncViewT

def aclient_required(client_view: AsyncViewT):
    @login_required(login_url = 'login')
    @wraps(client_view)
    async def fun(request: HttpRequest, *args, **kargs) -> HttpResponse:
        user = await aget_user(request)
        if user.is_authenticated and not user.is_writer:
            return await client_view(request, *args, **kargs)
        return HttpResponseForbidden('Only clients can access this view.')
    return fun


def awriter_required(writer_view: AsyncViewT):
    @login_required(login_url = 'login')
    @wraps(writer_view)
    async def fun(request: HttpRequest, *args, **kargs) -> HttpResponse:
        user = await aget_user(request)
        if user.is_authenticated and user.is_writer:
            return await writer_view(request, *args, **kargs)
        return HttpResponseForbidden('Only writers can access this view.')
    return fun
