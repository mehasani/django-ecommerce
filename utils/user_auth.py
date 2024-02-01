from functools import wraps

from django.http import HttpRequest
from django.shortcuts import redirect

from user_module.models import User


def LoggedinUser(request: HttpRequest):
    user_id = request.session.get('user_id')

    if user_id is not None and user_id != '':
        user: User = User.objects.filter(pk=user_id, is_active=True).first()
        if user is not None:
            return user
        else:
            return None
    else:
        return None


def user_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = LoggedinUser(request)
        if user:
            return view_func(request, *args, **kwargs)

        return redirect('login_page')

    return _wrapped_view
