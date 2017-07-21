from django.shortcuts import render
from django.shortcuts import HttpResponse
from app02 import models



def login(request):
    if request.method=='GET':
        return render(request,'login2.html')
    # role_list=models.User2Role.objects.filter(user__id=1).values('role_id')
    # for role in role_list:
    #     p1=models.Permission2Action2Role.objects.filter(role__id=role['role_id']).values('permission','action')
    #     for p in p1:
    #         v=models.Permission.objects.filter(id=p['permission']).values('url','caption','menu')
    #         print(v)
    else:
        permission_list=models.Permission2Action2Role.objects.filter(role__users__user_id=1).values('permission__url','action__code').distinct()

        dict = {}
        for obj in permission_list:
            dict[obj['permission__url']]=[]
        for row in permission_list:
            if row['permission__url'] in dict.keys():
                dict[row['permission__url']].append(row['action__code'])
    #{'/orders.html': ['get'], '/blogs.html': ['get', 'post'], '/users.html': ['post', 'get', 'edit', 'del']}
        request.session['permission']=dict
        return HttpResponse('登录成功')

def index(request):
    return HttpResponse('登录成功并有权限才能看到我')