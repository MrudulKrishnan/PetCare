from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path in ['/index/', '/another_protected_path/']:  # Add all protected paths here
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
    
class RedirectIfAuthenticatedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ['/r_login', '/'] and request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('staff_home')
            elif request.user.is_admin:
                return redirect('adm_home')
            else:
                return redirect('index')    