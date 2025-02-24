from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from common.django_utils import arender 
from common.auth import aclient_required

@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    
        return arender(request, 'client/dashboard.html')

