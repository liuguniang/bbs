from django.shortcuts import render,HttpResponse,redirect
from knowlage01 import models
from utils.pageinfo import PageInfo
from utils.random_check_code import rd_check_code
from knowlage01.forms import registerForm
from knowlage01.forms import new_articleForm
import os,json
from django.db.models import Count
from django.db.models import F
from utils.comment import comment_tree
from utils.xss import xss

#主页面     
def index(request,*args,**kwargs):
    # 获取当前URL
    # print(request.path_info)

    # models.article.objects.create(blog_id=1,title='世界上最好看的花',summary='新浪微博网民“白衣天使茉莉花”公布了一张照片。照片中，在破旧校门前，一个小女孩举着“遭性侵”的求助标语，地点是河南省周口市西华县奉母镇一中。',read_count=9,up_count=3,dowm_count=5,comment_count=8,classfiy_id=1,type=1)


   #登录成功后显示用户信息
    username=request.session.get('username')
    avator=models.user.objects.filter(nickname=username).values_list('avator').first()
    #页面显示文章类型
    condition={}
    type_id=int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    if type_id:
        condition['type']=type_id
    type_chioce=models.article.type_choice
    # 分页
    all_count = models.article.objects.filter(**condition).count()
    page_info = PageInfo(request.GET.get('page'), all_count, 5, '/')
    #文章详细信息
    article_list = models.article.objects.filter(**condition)[page_info.start():page_info.end()]

    #点赞最多文章
    up_article_list=models.article.objects.order_by('-up_count')[:5]


    #评论最多文章
    comment_article_list=models.article.objects.order_by('-comment_count')[:5]

    dict={'article_list':article_list,
          'type_chioce':type_chioce,
          'type_id':type_id,
          'page_info':page_info,
          'username':username,
          'avator':avator,
          'up_article_list':up_article_list,
          'comment_article_list':comment_article_list,

          }

    return render(request,'index.html',{'dict':dict})
#用户登录
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        code=request.POST.get('code')
        session_code=request.session.get('code')
        if code.upper()==session_code.upper():
            nickname=request.POST.get('username')
            password=int(request.POST.get('password'))
            obj=models.user.objects.filter(nickname=nickname).first()
            if obj.nickname==nickname and obj.password==password:
                request.session['username']=nickname
                return redirect('/')
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误'})
        else:
            return render(request, 'login.html', {'msg': '验证码错误'})
#用户注册
def register(request):
     if request.method=='GET':
         obj=registerForm(request)
         return render(request,'register.html',{'obj':obj})

     else:
         # 第一种方案：伪ajax提交用户头像信息
         # session_code = request.session.get('code')
         # #获取form组件生成的标签的值
         # obj = registerForm(request.POST)
         # #获取伪ajax生成的input标签的值（用户头像）
         # avator_path=request.POST.get('avator_path')
         # if obj.is_valid():
         #     code=obj.cleaned_data.pop('code')
         #     #判断验证码信息
         #     if session_code.upper()==code.upper():
         #         #向clean_data中加入一个键值对，存放用户头像信息
         #         obj.cleaned_data['avator']=avator_path
         #         #更新数据库
         #         models.user.objects.create(**obj.cleaned_data)
         #         return redirect('/')
         #     else:
         #         return render('register.html',{'msg': '验证码错误'})
         # else:
         #     return render(request, 'register.html', {'obj': obj})



         #第二种方案：本地预览头像，在form组件生成的标签中提交头像信息
         obj=registerForm(request,request.POST,request.FILES)
         if obj.is_valid():
             obj.cleaned_data.pop('code')
             obj.cleaned_data.pop('password2')
             models.user.objects.create(**obj.cleaned_data)
             return redirect('/')
         else:
             return render(request, 'register.html', {'obj': obj})
def register1(request):
    avator_obj = request.FILES.get('avator')

    file_path = os.path.join('static', 'img', avator_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in avator_obj.chunks():
            f.write(chunk)
            return HttpResponse(file_path)
#获取验证码
def check_code(request):
    #读取硬盘中的文件，在页面显示
    # f=open('static/img/flower.jpg','rb')
    # data=f.read()
    # f.close()
    # return HttpResponse(data)

    #创建图片，保存在本地，再读出来渲染
    # from PIL import Image
    # f=open('code.png','wb')
    # img=Image.new(mode='RGB',size=(120,30),color=(0,255,255))
    # img.save(f,'png')
    #
    # f=open('code.png','rb')
    # data=f.read()
    # f.close()
    # return HttpResponse(data)

    #创建图片，可以在上面画点，线，圆，写字，保存在内存中，直接读到页面进行渲染
    # from PIL import Image,ImageDraw,ImageFont
    # from io import BytesIO
    #
    # f=BytesIO()
    # img=Image.new(mode='RGB',size=(120,30),color=(255,255,255))
    # draw=ImageDraw.Draw(img,mode='RGB')
    # draw.point([10,10],fill='red')
    # draw.line((15,10,50,50),fill=(0,255,0))
    # draw.arc((0,0,30,30),0,360,fill='red')
    #
    #
    # font=ImageFont.truetype('static/font/domi.ttf',28)
    # draw.text([0, 0], 'python', 'red',font=font)
    # img.save(f,'png')
    # return HttpResponse(f.getvalue())

    #生成随机字符串
    # import random
    # char_list=[]
    # for i in range(5):
    #     char=chr(random.randint(65,90))
    #     char_list.append(char)
    #     font=ImageFont.truetype('static/font/domi.ttf',28)
    #     draw.text((i*24,0),char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
    # img.save(f,'png')
    # data=f.getvalue()
    # code=''.join(char_list)
    # request.session['code']=code
    # return HttpResponse(data)


    #引入验证码模块
    from io import BytesIO
    img,code=rd_check_code()
    stream=BytesIO()
    img.save(stream,'png')
    request.session['code']=code
    return HttpResponse(stream.getvalue())
#用户退出
def exit(request):
     key=request.session.session_key
     request.session.delete(key)
     return redirect('/')
#用户主页
def home(request,**kwargs):
    """
     http://127.0.0.1:8000/home.html
    :param request:
    :param site:  个人博客后缀
    :return:
    """
    site=kwargs.get('site')
    type=kwargs.get('type')
    typename=kwargs.get('typename')
    datetime=kwargs.get('datetime')

    #取用户相关信息
    user_list=models.user.objects.filter(blog__site=site).first()
    #获取当前用户博客
    blog=models.blog.objects.filter(site=site).first()
    #取粉丝数量
    fans_count=models.fans.objects.filter(faned__blog__site=site).values('faned__username').annotate(xx=Count('id'))
    focus_count=models.fans.objects.filter(fan__blog__site=site).values('fan__username').annotate(xx=Count('id'))

    #取标签分类
    # tag_list=models.tag.objects.filter(blog=blog)
    # for tag in tag_list:
    #     c=tag.article_tag_set.all().count
    #     print(c)
    tag_dict=models.article_tag.objects.filter(tag__blog__site=site).values('tag_id','tag__tag').annotate(xx=Count('id'))


    #取类型分类
    # classfiy_list=models.classfiy.objects.filter(blog=blog)
    # for classfiy in classfiy_list:
    #     d=classfiy.article_set.all().count()
    #     print(d)
    classfiy_dict=models.article.objects.filter(blog=blog).values('classfiy__id','classfiy__classfiy').annotate(xx=Count('aid'))


    #取日期分类
    #sqllite 数据库
    select={'month':'strftime("%%Y-%%m",create_time)'}
    date_list=models.article.objects.filter(blog=blog).extra(select=select).values('month').annotate(num=Count('aid'))
    #查询结果及sql语句
    # < QuerySet[{'month': '2017-07'    , 'num': 3}] >
    # SELECT(strftime("%Y-%m", create_time)) AS "month", COUNT("knowlage01_article"."aid") AS "num"
    # FROM "knowlage01_article"
    # WHERE "knowlage01_article"."blog_id" = 1
    # GROUP BY(strftime("%Y-%m", create_time))

    # mysql 数据库
    # select = {'month': 'date_format(create_time,"%%Y-%%m")'}
    # date_list = models.article.objects.filter().extra(select=select).values('month').annotate(num=Count('aid'))


    dict={
        'user_list':user_list,
        'tag_dict':tag_dict,
        'classfiy_dict':classfiy_dict,
        'fans_count':fans_count,
        'focus_count':focus_count,
        'blog':blog,
        'date_list':date_list,
    }

    if type=='classfiy':
        all_count = models.article.objects.filter(blog=blog,classfiy__id=typename).count()
        page_info = PageInfo(request.GET.get('page'), all_count, 2, typename + '.html')
        all_article_list=models.article.objects.filter(blog=blog,classfiy__id=typename)[page_info.start():page_info.end()]


    elif type=='tag':
        #自定义第三张表:自己反向关联article_tag表
        all_count = models.article.objects.filter(blog=blog,article_tag__tag_id=typename).count()
        page_info = PageInfo(request.GET.get('page'), all_count, 2, typename + '.html')
        all_article_list=models.article.objects.filter(blog=blog,article_tag__tag_id=typename)[page_info.start():page_info.end()]
        #通过M2M字段:直接通过m2m字段名从article表跨到tag表里
        # v=models.article.objects.filter(blog=blog,tags__id=typename)

    elif type=='datetime':
        #方法一：
        # all_count = models.article.objects.filter(blog=blog,create_time__startswith=typename).count()
        #方法二：
        all_count=models.article.objects.filter(blog=blog).extra(where=['strftime("%%Y-%%m",create_time)=%s'],params=[typename,]).count()
        page_info = PageInfo(request.GET.get('page'), all_count, 2, typename + '.html')
        all_article_list=models.article.objects.filter(blog=blog,create_time__startswith=typename)[page_info.start():page_info.end()]


    else:
        all_count = models.article.objects.filter(blog=blog).count()
        page_info = PageInfo(request.GET.get('page'), all_count, 2, site + '.html')
        all_article_list = models.article.objects.filter(blog=blog)[page_info.start():page_info.end()]

    return render(request,'home.html',{'page_info':page_info,'all_article_list': all_article_list,'dict':dict})
#文章最终页
def article(request,**kwargs):
    site=kwargs.get('site')
    typename=kwargs.get('typename')
    user_list=models.user.objects.filter(blog__site=site).first()
    blog=models.blog.objects.filter(site=site).first()
    fans_count=models.fans.objects.filter(faned__blog__site=site).values('faned__username').annotate(xx=Count('id'))
    focus_count=models.fans.objects.filter(fan__blog__site=site).values('fan__username').annotate(xx=Count('id'))
    tag_dict=models.article_tag.objects.filter(tag__blog__site=site).values('tag_id','tag__tag').annotate(xx=Count('id'))
    classfiy_dict=models.article.objects.filter(blog=blog).values('classfiy__id','classfiy__classfiy').annotate(xx=Count('aid'))
    #取日期分类
    select={'month':'strftime("%%Y-%%m",create_time)'}
    date_list=models.article.objects.filter(blog=blog).extra(select=select).values('month').annotate(num=Count('aid'))
    dict={
        'user_list':user_list,
        'tag_dict':tag_dict,
        'classfiy_dict':classfiy_dict,
        'fans_count':fans_count,
        'focus_count':focus_count,
        'blog':blog,
        'date_list':date_list,
    }
    article = models.content.objects.filter(article_id=int(typename)).first()
    comment_list = models.comment.objects.filter(article_id=int(typename)).values('id', 'create_time', 'content',
                                                                                  'user__nickname','parent_id_id')
    comment_dict = {}
    for item in comment_list:
        item['child'] = []
        comment_dict[item['id']] = item
    comment = []
    for item in comment_list:
        pid = item['parent_id_id']
        if pid:
            comment_dict[pid]['child'].append(item)
        else:
            comment.append(item)

    comment_str=comment_tree(comment)
    return render(request, 'detail.html', {'comment_str': comment_str, 'article': article, 'dict': dict})
#前端进行评论的处理
def comment(request):
    typename=request.POST.get('typename')
    comment_list = models.comment.objects.filter(article_id=int(typename)).values("id", "content",
                                                                                  "user__nickname", "parent_id_id")
    comment_dict = {}
    for item in comment_list:
        item["child"] = []
        comment_dict[item['id']] = item
    comment = []
    for item in comment_list:
        pid = item["parent_id_id"]
        if pid:
            comment_dict[pid]["child"].append(item)
        else:
            comment.append(item)
    return HttpResponse(json.dumps(comment))
#点赞
def up(request):
    username=request.session.get('username')
    status = {'msg': '', 'type': None}
    if username:
        obj=models.user.objects.filter(nickname=username).first()
        type=request.POST.get('type')

        if type=='Y':
            id = request.POST.get('id')
            try:
                from django.db import transaction
                with transaction.atomic():
                    models.updown.objects.create(article_id=id,user_id=obj.uid,type=True)
                    models.article.objects.filter(aid=id).update(up_count=F('up_count')+1)
                status['msg']='点赞成功'
                status['type']='True'
                return HttpResponse(json.dumps(status))
            except Exception as e:
                if models.updown.objects.filter(article_id=id,user_id=obj.uid,type=True).first():
                    status['msg']='您已经点过赞了'
                    return HttpResponse(json.dumps(status))
                else:
                    status['msg']='您已经点过踩了，不能点赞了'
                    return HttpResponse(json.dumps(status))
        else:
            id = request.POST.get('id')
            try:
                from django.db import transaction
                with transaction.atomic():
                    models.updown.objects.create(article_id=id,user_id=obj.uid,type=False)
                    models.article.objects.filter(aid=id).update(dowm_count=F('dowm_count')-1)
                status['msg'] = '点踩成功'
                status['type'] = 'False'
                return HttpResponse(json.dumps(status))
            except Exception as e:
                if models.updown.objects.filter(article_id=id,user_id=obj.uid,type=False).first():
                    status['msg']='您已经点过踩了'
                    return HttpResponse(json.dumps(status))
                else:
                    status['msg']='您已经点过赞了，不能点踩了'
                    return HttpResponse(json.dumps(status))
    else:
        status['msg']='请先登录'
        return HttpResponse(json.dumps(status))
# 后台管理
def admin(request,**kwargs):
    #组合筛选条件
    condition={}
    for k,v in kwargs.items():
        kwargs[k]=int(v)        #将字符串转换为数字
        if v:
            condition[k]=v

    #分类标签列表
    username=request.session.get('username')
    blog=models.blog.objects.filter(user__username=username)
    type_list=models.article.type_choice
    classfiy_list=models.classfiy.objects.filter(blog=blog)
    tag_list=models.tag.objects.filter(blog=blog)
    #筛选结果
    condition['blog']=blog
    article_list=models.article.objects.filter(**condition)
    dict={
        'type_list':type_list,
        'classfiy_list':classfiy_list,
        'tag_list':tag_list,
        'kwargs':kwargs,                      #返回上一次的筛选条件
        'article_list':article_list,
    }
    return render(request,'admin.html',{'dict':dict})
#添加新随笔（kindeditor插件）
CONTENT=""
def new_article(request):
    if request.method=='GET':
        if request.session.get('username'):
            obj=new_articleForm(request)
            return render(request,'new_article.html',{'obj':obj})
        else:
            return redirect('/')
    else:
        obj=new_articleForm(request,request.POST)
        # title=request.POST.get('title')
        # content=request.POST.get('content')
        # global CONTENT
        # CONTENT = content
        print('dddddd')
        if obj.is_valid():
            article_list=obj.cleaned_data
            print(article_list)

            return HttpResponse('上传文章成功')
        else:
            return render(request, 'new_article.html', {'obj': obj})
#查看新随笔的内容（beautifulsoup过滤）
def see_article(request):
    content=xss(CONTENT)
    return render(request, 'see_article.html', {'content':content})

def upload_img(request):
    upload_type=request.GET.get('dir')    #查看上传过来的文件类型
    file_obj=request.FILES.get('fafafa')
    file_path=os.path.join('static/img',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    #返回编辑器认识的数据类型（图片保存的路径）
    dic = {
        'error': 0,
        'url': '/' + file_path,
        'message': '错误了...'
    }

    return HttpResponse(json.dumps(dic))
