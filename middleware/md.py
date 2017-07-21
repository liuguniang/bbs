from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re

class M1(MiddlewareMixin):
    def process_request(self,request,*args,**kwargs):
        valid=['/app02/login/','/','/app02/index/']
        if request.path_info not in valid:
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