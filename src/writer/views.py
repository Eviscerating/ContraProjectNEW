from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from common.django_utils import arender
from common.auth import awriter_required

@awriter_required
async def dashboard(request: HttpRequest) -> HttpResponse:
            return await arender(request, 'writer/dashboard.html')
