from django import forms
from firstapp.models import Article, Comment, Keeper, Salary, Order, User, ServiceComment
from django.core.exceptions import ValidationError

#widget=forms.Textarea(评论，聊天)
# 注册表单及校验
def email_validator(email):
    for char in email:
        if char == '@':
            break
    else:
        raise ValidationError('请输入有效的邮箱')

def email_repeat(email):
    emailrepeat=User.objects.filter(email=str(email))
    if len(emailrepeat) > 0:
        raise ValidationError('邮箱已被注册，请重新输入')

def phone_repeat(phone):
    phonerepeat=User.objects.filter(phone_number=str(phone))
    if len(phonerepeat) > 0 :
        raise ValidationError('手机号码已被注册，请重新输入')

def phone_length(phone):
    if len(phone) != 11 :
        raise ValidationError('请输入有效的手机号码')

class signForm(forms.Form):
    name=forms.CharField(label="昵称",max_length=10)
    email=forms.CharField(label="邮箱",validators=[email_validator,email_repeat])
    phone=forms.CharField(label="电话号码",max_length=11,
                            validators=[phone_repeat,phone_length])
    code=forms.CharField(label="密码",max_length=20)


#登录表单及校验
def email_exists(email):
    emailexists=User.objects.filter(email=email)
    if len(emailexists) == 0:
        raise ValidationError('邮箱不存在，请重新输入')

class loginForm(forms.Form):
    email=forms.CharField(label="电子邮箱",validators=[email_exists])
    code=forms.CharField(max_length=20,label="密码")

#发布图片表单
class imageForm(forms.Form):
    头像=forms.ImageField()