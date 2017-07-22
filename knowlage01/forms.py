

from django.core.exceptions import ValidationError
from django.forms import Form,widgets,fields
from knowlage01 import models
from bs4 import BeautifulSoup

class registerForm(Form):

    username = fields.CharField(max_length=64,
                                widget=widgets.TextInput(attrs={'class':'form-control'}))
    password = fields.IntegerField(widget=widgets.PasswordInput(attrs={'class':'form-control'}))
    password2 = fields.IntegerField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}))

    nickname = fields.CharField(max_length=64,widget=widgets.TextInput(attrs={'class':'form-control'}))

    email = fields.EmailField(widget=widgets.EmailInput(attrs={'class':'form-control'}))
    avator=fields.FileField(widget=widgets.FileInput(attrs={'id':'imgselect'}))
    code=fields.CharField(max_length=6,widget=widgets.TextInput(attrs={'class':'form-control'}))


    def __init__(self,request,*args,**kwargs):
        super(registerForm,self).__init__(*args,**kwargs)
        self.request=request
    def clean_code(self):
        input_code=self.cleaned_data['code']
        session_code=self.request.session.get('code')
        if input_code.upper()==session_code.upper():
            return input_code
        raise ValidationError('验证码错误')
    def clean(self):
        p1=self.cleaned_data.get('password')
        p2=self.cleaned_data.get('password2')
        if p1==p2:
            return None
        #给某一个字段添加错误信息
        self.add_error('password2',ValidationError('密码不一致'))

class new_articleForm(Form):
    title=fields.CharField(max_length=64)
    summary=fields.CharField(min_length=128,max_length=264)
    content=fields.CharField(
        widget=widgets.Textarea(attrs={'id':'i1'})
    )

    type=fields.IntegerField(
        widget=widgets.Select(choices=tuple(models.article.type_choice))
    )
    classfiy_id=fields.ChoiceField(
        # choices=tuple(models.classfiy.objects.filter().values_list('id','classfiy')),
        widget=widgets.Select
    )
    tag=fields.MultipleChoiceField(
        # choices=tuple(models.tag.objects.values_list('tid','tag')),
        widget=widgets.CheckboxSelectMultiple
    )
    def __init__(self,request,*args,**kwargs):
        super(new_articleForm,self).__init__(*args,**kwargs)
        self.request=request
        username = self.request.session.get('username')
        blog = models.blog.objects.filter(user__username=username)
        self.fields['classfiy_id'].choices=tuple(models.classfiy.objects.filter(blog=blog).values_list('id','classfiy'))
        self.fields['tag'].choices=tuple(models.tag.objects.filter(blog=blog).values_list('tid','tag'))
    def clean_content(self):
        valid_tag = {
            'p': ['class', 'id'],
            'img': ['href', 'alt', 'src'],
            'div': ['class']
        }
        content=self.cleaned_data['content']
        soup = BeautifulSoup(content, 'html.parser')

        tags = soup.find_all()
        for tag in tags:
            if tag.name not in valid_tag:
                tag.decompose()
            if tag.attrs:
                for k in list(tag.attrs.keys()):
                    if k not in valid_tag[tag.name]:
                        del tag.attrs[k]

        content_str = soup.decode()
        return content_str