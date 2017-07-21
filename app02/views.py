from django.shortcuts import render
from django.shortcuts import HttpResponse
from app02 import models
import re


def login(request):
    if request.method=='GET':
        return render(request,'login2.html')
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


def menu(request):
    """
    需要用户名或id，产出：用户关联的所有的菜单
    :param request:
    :return:
    """
    #所有菜单
    all_menu_list=models.Menu.objects.all().values('id','caption','parent_id')
    # < QuerySet[{'parent_id': None, 'id': 1, 'caption': '菜单一'},
    # {'parent_id': None, 'id': 2, 'caption': '菜单二'},
    # { 'parent_id': 1, 'id': 3, 'caption': '菜单11'}] >


    # 与用户有关联的权限
    # user=models.User.objects.filter(id=1).first()
    # role_list=models.Role.objects.filter(users__user=user)
    # permission_list=models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url','permission__caption','permission__id','permission__menu_id')

    permission_list=models.Permission2Action2Role.objects.filter(role__users__user_id=1).values('permission__url',
                                  'permission__caption','permission__id','permission__menu_id').distinct()
    # [{'permission__caption': '用户管理', 'permission__id': 1, 'permission__menu_id': 3, 'permission__url': '/users.html'},
    #  {'permission__caption': '用户管理', 'permission__id': 1, 'permission__menu_id': 3, 'permission__url': '/users.html'},]

     ####################将权限挂靠到菜单上
    all_menu_dict={}
    for row in all_menu_list:
        row['child']=[]
        row['status']=False  # 是否显示菜单
        row['opened']=False  # 是否默认打开
        all_menu_dict[row['id']]=row
        # {1: {'opened': False, 'status': False, 'child': [], 'parent_id': None, 'id': 1, 'caption': '菜单一'},
        #  2: {'opened': False, 'status': False, 'child': [], 'parent_id': None, 'id': 2, 'caption': '菜单二'},
        #  3: {'opened': False, 'status': False, 'child': [], 'parent_id': 1, 'id': 3, 'caption': '菜单11'}}
    for per in permission_list:
        if not per['permission__menu_id']:
            continue

        item={
            'id':per['permission__id'],
            'caption':per['permission__caption'],
            'parent_id':per['permission__menu_id'],
            'url':per['permission__url'],
            'status':True,
            'opened':False
        }
        if re.match(per['permission__url'],'/users.html'):
            item['opened']=True
        # 将权限挂靠到菜单上
        pid=item['parent_id']
        all_menu_dict[pid]['child'].append(item)


    # {1: {'opened': False,'parent_id': None, 'id': 1, 'caption': '菜单一', 'status': False
    #      'child': [{'url': '/blogs.html', 'parent_id': 1, 'opened': False, 'status': True, 'caption': '博客管理', 'id': 3}],},
        #将当前权限前辈status= True
        temp = pid
        while not all_menu_dict[temp]['status']:
            all_menu_dict[temp]['status']=True
            temp=all_menu_dict[temp]['parent_id']
            if not temp:
                break
        #将当前权限前辈opened=True
        if item['opened']:
            temp = pid
            while not all_menu_dict[temp]['opened']:
                all_menu_dict[temp]['opened'] = True
                temp = all_menu_dict[temp]['parent_id']
                if not temp:
                    break
    # 对处理后的菜单表进行层级关系处理
    result=[]
    for row in all_menu_list:
        pid=row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)
    # 结构化处理结果
    for row in result:
        print(row['caption'],row['status'],row['opened'],row)

    # 通过结构化处理，生成菜单
    """
    status=False ,不生产成
    opened=True  ,true不加，false，加hide

    <div class='menu-item'>
        <div class='menu-header'>菜单1</div>
        <div class='menu-body %s'>
            <a>权限1</a>
            <a>权限2</a>
             <div class='menu-item'>
                <div class='menu-header'>菜单11</div>
                <div class='menu-body hide'>
                    <a>权限11</a>
                    <a>权限12</a>
                </div>
            </div>
        </div>
    </div>
    """
    def menu_tree(menu_list):
        tpl1="""
        <div class='menu-item'>
            <div class='menu-header'>{0}</div>
            <div class='menu-body {2}'>{1}</div>
        </div>
        """
        tpl2="""
        <a href='{0}' class='{1}'>{2}</a>
        """
        menu_str=''
        for menu in menu_list:
            if not menu['status']:
                continue
            if menu.get('url'):
                menu_str += tpl2.format(menu['url'],'active' if menu['opened'] else '',menu['caption'])
            else:
                if menu['child']:
                    child_html=menu_tree(menu['child'])
                else:
                    child_html=''
                menu_str += tpl1.format(menu['caption'],child_html,'' if menu['opened'] else 'hide')
        return menu_str
    menu_html=menu_tree(result)
    return render(request,'menu.html',{'menu_html':menu_html})


















