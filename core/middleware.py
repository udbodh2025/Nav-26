from django.shortcuts import redirect
from django.urls import resolve
from .models import Module

class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            resolved = resolve(request.path_info)
            if resolved.url_name == 'module':
                module_id = resolved.kwargs.get('module_id')
                if module_id:
                    module = Module.objects.get(id=module_id)
                    if not request.user.groups.filter(id__in=module.menu_item.groups.all()).exists() and module.menu_item.groups.exists():
                        return redirect('home')
        
        response = self.get_response(request)
        return response

