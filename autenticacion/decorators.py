from django.shortcuts import redirect

def role_required(role_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect('acceso_denegado')  # Redirigir a una página de acceso denegado
        return _wrapped_view
    return decorator
