from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

# def allowed_users(allowed_roles=[]):
#     def decorator(view_function):
#         def wrapper_function(request, *args, **kwargs):

#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name

#             if group in allowed_roles:
#                 return view_function(request, *args, **kwargs)
#             else:
#                 return HttpResponse('No Authorization ')
#         return wrapper_function
#     return decorator


def allowed_users(allowed_roles=['admin']):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            try:
                request.user.groups.exists()
            except:
                request = args[0]

            group = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    if group.name in allowed_roles:
                        return view_function(request, *args, **kwargs)
            return HttpResponseForbidden()
        return wrapper_function
    return decorator