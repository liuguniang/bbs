from rbac import models
from django.utils.safestring import mark_safe
import re

def permission_session(user_id,request):
    """
    用户登录时在session中设置用户权限
    :param user_id: rbac的user表中的用户id
    :param request:
    :return:
    """
    permission_list = models.Permission2Role2Action.objects.filter(role__users__user_id=user_id).values('permission__url',
                                                                                             'action__code').distinct()
    dict = {}
    for obj in permission_list:
        dict[obj['permission__url']] = []
    for row in permission_list:
        if row['permission__url'] in dict.keys():
            dict[row['permission__url']].append(row['action__code'])
            # {'/orders.html': ['get'], '/blogs.html': ['get', 'post'], '/users.html': ['post', 'get', 'edit', 'del']}
    request.session['permission'] = dict

def menu(user_id,current_url):
    """
        根据id，当前访问的url,产出：用户关联的所有的菜单
        :param request:
        :return:
        """
    # 所有菜单
    all_menu_list = models.Menu.objects.all().values('id', 'caption', 'parent_id')
    permission_list = models.Permission2Role2Action.objects.filter(role__users__user_id=user_id).values('permission__url',                                                                                    'permission__caption',
                                                                                                  'permission__id'                                                                                        'permission__menu_id').distinc
    ####################将权限挂靠到菜单上
    all_menu_dict = {}
    for row in all_menu_list:
        row['child'] = []
        row['status'] = False  # 是否显示菜单
        row['opened'] = False  # 是否默认打开
        all_menu_dict[row['id']] = row
    for per in permission_list:
        if not per['permission__menu_id']:
            continue

        item = {
            'id': per['permission__id'],
            'caption': per['permission__caption'],
            'parent_id': per['permission__menu_id'],
            'url': per['permission__url'],
            'status': True,
            'opened': False
        }
        if re.match(per['permission__url'],current_url):
            item['opened'] = True
        # 将权限挂靠到菜单上
        pid = item['parent_id']
        all_menu_dict[pid]['child'].append(item)
        # 将当前权限前辈status= True
        temp = pid
        while not all_menu_dict[temp]['status']:
            all_menu_dict[temp]['status'] = True
            temp = all_menu_dict[temp]['parent_id']
            if not temp:
                break
        # 将当前权限前辈opened=True
        if item['opened']:
            temp = pid
            while not all_menu_dict[temp]['opened']:
                all_menu_dict[temp]['opened'] = True
                temp = all_menu_dict[temp]['parent_id']
                if not temp:
                    break
    # 对处理后的菜单表进行层级关系处理
    result = []
    for row in all_menu_list:
        pid = row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)
    # 通过结构化处理，生成菜单
    def menu_tree(menu_list):
        tpl1 = """
            <div class='menu-item'>
                <div class='menu-header'>{0}</div>
                <div class='menu-body {2}'>{1}</div>
            </div>
            """
        tpl2 = """
            <a href='{0}' class='{1}'>{2}</a>
            """
        menu_str = ''
        for menu in menu_list:
            if not menu['status']:
                continue
            if menu.get('url'):
                menu_str += tpl2.format(menu['url'], 'active' if menu['opened'] else '', menu['caption'])
            else:
                if menu['child']:
                    child_html = menu_tree(menu['child'])
                else:
                    child_html = ''
                menu_str += tpl1.format(menu['caption'], child_html, '' if menu['opened'] else 'hide')
        return menu_str

    menu_html = menu_tree(result)
    return mark_safe(menu_html)

def css():
    css="""
        <style>
        .hide{
            display: none;
        }
        .active{
            color: red;
        }
        .menu-body{
            margin-left: 20px;
        }
        .menu-body a{
            display: block;
        }
    </style>
    """
    return mark_safe(css)
def js():
    js="""
    <script>
    $(function(){
        $('.menu-header').click(function(){
            $(this).next().removeClass('hide').parent().siblings().find('.menu-body').addClass('hide');
        })
    })
</script>
    """
    return mark_safe(js)
