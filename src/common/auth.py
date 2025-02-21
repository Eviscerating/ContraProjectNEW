from functools import wraps 

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from django.shortcuts import redirect
from common.django_utils import AsyncViewT
from django.core.exceptions import ObjectDoesNotExist

from account.models import CustomUser
from .django_utils import AsyncViewT


#def aclient_required(client_view: AsyncViewT):
 #   @login_required(login_url = 'login')
  #  @wraps(client_view)
   # async def fun(request: HttpRequest, *args, **kargs) -> HttpResponse:
    #    user = await aget_user(request)
     #   if user.is_authenticated and not user.is_writer:
      #      return await client_view(request, *args, **kargs)
       # return HttpResponseForbidden('Only clients can access this view.')
    #return fun


#def awriter_required(writer_view: AsyncViewT):
 #   @login_required(login_url = 'login')
  #  @wraps(writer_view)
   # async def fun(request: HttpRequest, *args, **kargs) -> HttpResponse:
    #    user = await aget_user(request)
     #   if user.is_authenticated and user.is_writer:
      #      return await writer_view(request, *args, **kargs)
       # return HttpResponseForbidden('Only writers can access this view.')
  #  return fun
  
def aclient_required(client_view: AsyncViewT):
    return aprofile_required('client')(client_view)  
  
def awriter_required(writer_view: AsyncViewT):
    return aprofile_required('writer')(writer_view)
  
USER_PROFILES = {
    'client': lambda user: not user.is_writer,
    'writer': lambda user: user.is_writer,
}
  
  
def aprofile_required(profile: str, login_url: str = 'login'):
    if profile not in USER_PROFILES:
        raise ValueError(f'Invalid profile: {profile}')
    is_of_profile = USER_PROFILES[profile]
    def decorator (view: AsyncViewT):
        @login_required(login_url = login_url)
        @wraps(view)
        async def async_view(request: HttpRequest, *args, **kargs) -> HttpResponse:
            user: CustomUser = await aget_user(request)
            if user.is_authenticated and is_of_profile(user):
                return await view(request, *args, **kargs)
            return HttpResponseForbidden(f"Only members of '{profile}' can access this view.")
        return async_view
    return decorator

def ensure_for_current_user(model: type, *, id_in_url: str = 'id', redirect_if_missing: str):
    def decorator (view: AsyncViewT):
        async def async_view(request: HttpRequest, *args, **kargs) -> HttpResponse:
            obj_id = kargs[id_in_url]
            user = await aget_user(request)
            try:
                obj = await model.objects.aget(id = obj_id, user = user)
                del kargs [id_in_url]
                return await view (request, obj, *args, **kargs)
            except ObjectDoesNotExist:
                return redirect(redirect_if_missing)
        return async_view
    return decorator
