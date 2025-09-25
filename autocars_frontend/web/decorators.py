from django.shortcuts import redirect
from functools import wraps

def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("token"):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper
