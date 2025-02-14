from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user # type: ignore

from common.auth import aclient_required

@aclient_required
@login_required(login_url = 'login') # type: ignore
async def dashboard(request: HttpRequest) -> HttpResponse:
    
        return render(request, 'client/dashboard.html')

