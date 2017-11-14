from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re
from rbac import conf
class RbacMiddleWare(MiddlewareMixin):
    def process_request(self,request,*args,**kwargs):
        for pattern in conf.VALID_URL:
            if re.match(pattern,request.path_info):
                return None

        action=request.GET.get('md')
        permission=request.session.get('permission')
        if not permission:
            return HttpResponse('无权限')
        flag=False
        for k,v in permission.items():
            if re.match(k,request.path_info):
                if action in v:
                    flag=True
                    break
        if not flag:
            return HttpResponse('无权限')