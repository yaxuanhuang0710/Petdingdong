from __future__ import unicode_literals
from django import forms
from django.shortcuts import HttpResponse, render,redirect
from django.template import Context, Template
from firstapp.form import signForm,loginForm
from firstapp.models import (Article, Comment, Keeper, Order, Salary, ServiceComment, User,Chat)
#from django.core.paginator import Paginator
from django.template import RequestContext
from django.utils import timezone
from datetime import timedelta
from PIL import Image
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import random
from django.db.models import Count, Q #不知道有什么用

from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

def main(request):
    context={}
    article_list=Article.objects.all().order_by('-articleNo')[:6]
    context['article_list']=article_list
    main_page = render(request, 'first_landing_page.html',context)
    return main_page

def mainin(request):
    context={}

    login_No=request.session.get('login_No','')#########新加的
    keeperNo=request.session.get('keeperNo','')
    orderNo=request.session.get('orderNo','')
    date=timezone.now()
    if request.method == 'POST':
        score=float(request.POST.get('score',""))
        comment=request.POST.get('comment',"")
        c=ServiceComment(customerNo=login_No,keeperNo=keeperNo,orderNo=orderNo,score=score,co_time=date,comment=comment)
        c.save()
        Order.objects.filter(orderNo=orderNo).update(state="已完成")
        Ke=Keeper.objects.filter(keeperNo=keeperNo)
        for k in Ke:
            ks=k.star
        ks=(0.4*ks+0.6*score)
        Keeper.objects.filter(keeperNo=keeperNo).update(star=ks)
        #keeper评分


    #login_No=request.session.get('login_No','')#########等

    context['login_No']=login_No#######新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    article_list=Article.objects.all().order_by('-articleNo')[:6]
    context['article_list']=article_list
    mainin_page = render(request, 'first_landing_page1.html',context)
    return mainin_page

def denglu(request):
    context={}
    #login_No="2"#需修改：放在登录成功后，改变量，再加入context
    #request.session['login_No']=login_No#同上
    form = loginForm()
    
    context['form']=form
    if request.method == 'POST':
        form=loginForm(request.POST)
        context['form']=form
        if form.is_valid():
            email=form.cleaned_data['email']
            code=form.cleaned_data['code']
            userResult=User.objects.filter(email=email,code=code)
            if len(userResult)>0:
                for user in userResult:
                    login_No=user.No
                request.session['login_No']=login_No
                context['login_No']=login_No
                return redirect('/mainin/',{'login_No':login_No})
            else:
                return HttpResponse("该用户不存在，请重新输入")
        else:
            return render(request,'denglu.html',context)
    return render(request,"denglu.html",context)

def zhuce(request):
    context={}
    form = signForm()
    context['form']=form
    if request.method == 'POST':
        form=signForm(request.POST)
        context['form']=form
        if form.is_valid():
            No=User.objects.count()+1
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            telephone=form.cleaned_data['phone']
            code=form.cleaned_data['code']
            u=User(No=No,ID=name,code=code,email=email,phone_number=telephone)
            u.save()
            return redirect('/denglu/')
        else:
            return render(request,'zhuce.html',context)
    return render(request,"zhuce.html",context)

def search(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    search_page = render(request, 'search.html',context)####新加
    return search_page

def searchResult(request):
    pettype=request.GET['petType']
    starttime=request.GET['startTime']
    endtime=request.GET['endTime']
    servicetype=request.GET['serviceType']
    dist=request.GET['district']
    address=request.GET['address']
    request.session['starttime']=starttime
    request.session['endtime']=endtime
    request.session['address']=address
    Keeper_list = Keeper.objects.filter(district=dist,pet_type=pettype).order_by('-star')# [:6]需要连search的表单结果
    Salary_list=Salary.objects.filter(service_type=servicetype) 
   # paginator = Paginator(Keeper_list,6)#分页
    #context = {'Keeper_list': Keeper_list,'Salary_list': Salary_list }
    login_No=request.session.get('login_No','')#########新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context = {'Keeper_list': Keeper_list,'Salary_list': Salary_list, 'pettype':pettype,'starttime':starttime,'endtime':endtime,'servicetype':servicetype,'dist':dist ,'address':address,
    'login_User':login_User,'login_No':login_No}
    searchResult_page = render(request, 'searchResult.html',context)
    return searchResult_page

def sitterInfo(request):
    keeperNo=request.GET['keeperNo']
    request.session['keeperNo']=keeperNo
    starttime=request.session.get('starttime','2012-01-01')
    endtime=request.session.get('endtime','2012-02-02')
    address=request.session.get('address','12')
    servicetype=request.session.get('servicetype','遛狗')

    keeper= Keeper.objects.filter(keeperNo=keeperNo)
    Salary_list=Salary.objects.filter(keeperNo=keeperNo)
    comment=ServiceComment.objects.filter(keeperNo=keeperNo)
    User_list=User.objects.all() 
    atm='1'
    request.session['atm']=atm
    
    login_No=request.session.get('login_No','')#########新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context = {'keeper': keeper, 'comment':comment, 'Salary_list': Salary_list,
      'User_list':User_list, 'keeperNo':keeperNo,'starttime':starttime,'endtime':endtime,'address':address,
      'login_User':login_User,'login_No':login_No,'servicetype':servicetype,'atm':atm}
    sitterInfo_page = render(request, 'sitterInfo.html',context)
    return sitterInfo_page
    
def Help(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    Help_page = render(request, 'Help.html',context)####新加
    return Help_page

def sitterHelp(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    sitterHelp_page = render(request, 'sitterHelp.html',context)####新加
    return sitterHelp_page

def identification(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    identification_page = render(request, 'identification.html',context)####新加
    return identification_page

'''def save(request):
    a = request.GET#获取get()请求
    name = a.get('name')
    #print(userName,passWord)
    #连接数据库
    db = pymysql.connect('127.0.0.1','root','123','db2')#创建游标
    cursor = db.cursor()#SQL语句
    sql1 = 'insert into Keeper values(%s)'#执行SQL语句
    cursor.execute(sql1,(name))
    db.commit()
    cursor.close()
    db.close()
    return HttpResponse('注册成功')'''

def keeper(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    if request.method == "POST":
        name=request.POST.get("name","")
        keeper1=Keeper()
        keeper1.name=name
        keeper1.save() 
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    return render(request, "identification.html",context)####新加


'''def keeper(request):
    if request.method == "POST":
        name=request.POST.get("name","")
        Keeper.objects.create(name=name)

    return render(request, "identification.html")'''

def single(request):
    context={}####新加
    aN=request.GET['articleNo']
    article =Article.objects.filter(articleNo=aN)
    Comment_list=Comment.objects.filter(articleNo=aN)
    User_list=User.objects.all()
    context = {'article': article,'User_list':User_list,'Comment_list':Comment_list}
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    context['article_id']=aN
    if request.method == 'POST':
        #userNo='1'######删
        time=timezone.now()
        text=request.POST.get('text',"")
        a=Comment(articleNo=aN,userNo=login_No,time=time,text=text)
        a.save()
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    single_page = render(request, 'single.html', context)
    return single_page

def multi(request):
    login_No=request.session.get('login_No','')#########新加的
    login_User=User.objects.filter(No=login_No)######新加的
    Article_list =Article.objects.all().order_by('-articleNo')
    User_list=User.objects.all()
    context = {'Article_list': Article_list,'User_list':User_list,'login_User':login_User,'login_No':login_No}
    multi_page = render(request, 'multi.html',context)
    return multi_page

def forgetpassword(request):
    if request.method == 'POST':
        s="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        rand=random.sample(list(s),6)
        rand="".join(rand)
        request.session['验证码']=rand
        email=request.POST.get("email","")
        email_exists=User.objects.filter(email=email)              
        if len(email_exists) > 0 :
            for user in email_exists:###for循环获取LoginNo
                No=user.No
            from_email = settings.DEFAULT_FROM_EMAIL
            subject = '来自宠叮咚的密码重置验证码'
            text_content = '您的验证码是'+rand
            html_content = '<p>您的验证码是:<strong>'+rand+'</strong></p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            res=msg.send()
            if res == 1:
                request.session['login_No']=No
                return HttpResponse('邮件发送成功')
            else:
                return HttpResponse('邮件发送失败')
        else:
            return HttpResponse('邮箱不存在，请重新输入!')
    forgetpassword_page = render(request, 'forgetpassword.html')#,{'login_No':login_No})
    return forgetpassword_page

def forgetpassword2(request):
    if request.method == 'POST':
        rand=request.session.get("验证码")
        real=request.POST.get("yanzhengma")
        if real == str(rand) :
            login_No=request.session.get("login_No")
            return render(request, 'forgetpassword2.html',{'login_No':login_No})
        else:
            return HttpResponse("验证码不符，请重新输入")
            #return render(request,"forgetpassword.html",{state:"验证码不符，请重新输入"})
    else:
        return render(request,"forgetpassword2.html")

def forgetpassword3(request):
    login_No=request.session.get("login_No")
    if request.method == 'POST':
        newpassword=request.POST.get("password")
        User.objects.filter(No=login_No).update(code=newpassword)
    forgetpassword3_page = render(request,'forgetpassword3.html')
    return forgetpassword3_page

def order(request):
    
    
    login_No=request.session.get('login_No','')#########新加的
    keeperNo=request.session.get('keeperNo','')
    starttime=request.session.get('starttime','2012-01-01')
    endtime=request.session.get('endtime','2012-02-02')
    address=request.session.get('address','12')
    servicetype=request.session.get('servicetype','遛狗')
    num=Order.objects.count()+1
    
    money=Salary.objects.filter(keeperNo=keeperNo,service_type=servicetype)#[0][3]
    
    atm=request.session.get('atm','0')
    #print(atm*20)
    if atm == "1":
        for m in money:
            s=m.salary
        a=Order(keeperNo=keeperNo,start_time=starttime,end_time=endtime,
        orderNo=num,customerNo=login_No,money=s,address=address,state='正在进行')
        a.save()
        del request.session['atm']

    if request.method == 'POST':
        head_img=request.FILES.get("img","")
        img =Image.open(head_img)
        img_name = str(head_img).replace("/", "_")
        img_path = "static/user_img/" + str(login_No) + "_" + img_name
        img.save(img_path)# 用于保存到数据库的地址，为了调用做出改动
        img_path_save = "static/user_img/" + str(login_No) + "_" + img_name
        User.objects.filter(No=login_No).update(image=img_path_save)  
    
    User_list=User.objects.filter(No=login_No)##需修改成变量
    User_list1=User.objects.all()##需修改成变量
    Order_list1=Order.objects.all().order_by('-orderNo')
    Keeper_list=Keeper.objects.all()
    Keeper_li=Keeper.objects.filter(realNo=login_No)
    login_User=User.objects.filter(No=login_No)######新加的
    context = {'User_list':User_list,'User_list1':User_list1,'Order_list1':Order_list1,
    'Keeper_list':Keeper_list,'keeperNo':keeperNo,'login_No':login_No,'login_User':login_User,'servicetype':servicetype,'Keeper_li':Keeper_li}
    order_page = render(request, 'order.html', context)
    return order_page
    
'''def pmain(request):
    User_list=User.objects.filter(No='1')##需修改成变量
    Article_list=Article.objects.filter(authorNo='1')##需修改成变量
    user=User.objects.get(No='1')##需修改成变量
    img=user.image
    if request.method == 'POST':
        form=imageForm(request.POST,request.FILES)
        if form.is_valid():
            img=form.cleaned_data['头像']#
            User.objects.filter(No='1').update(image=img)
        else:
            return HttpResponse("上传失败！")
    else:
        form=imageForm()
    context = {'User_list':User_list, 'Article_list': Article_list,'form':form,'img':img}
    pmain_page = render(request, 'pmain.html',context)
    return pmain_page'''

def pmain(request):
    login_No=request.session.get('login_No','')#########新加的
    login_User=User.objects.filter(No=login_No)######新加的
    Article_list=Article.objects.filter(authorNo=login_No).order_by('-articleNo')##需修改成变量
    if request.method == 'POST':
        head_img=request.FILES.get("img","")
        img =Image.open(head_img)
        img_name = str(head_img).replace("/", "_")
        img_path = "static/user_img/" + str(login_No) + "_" + img_name
        img.save(img_path)# 用于保存到数据库的地址，为了调用做出改动
        img_path_save = "static/user_img/" + str(login_No) + "_" + img_name
        User.objects.filter(No=login_No).update(image=img_path_save)       
    context = {'Article_list': Article_list,'login_User':login_User,'login_No':login_No}
    pmain_page = render(request, 'pmain.html',context)
    return pmain_page

def newarticle(request):
    context={}
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    if request.method == 'POST':
        articleNo=Article.objects.count()+1
        # authorNo=4 #新s的        
        headline=request.POST.get('title',"")
        content =request.POST.get('content',"")
        article_type=request.POST.get('article_type',"")
        image_obj = request.FILES.get('upload_img')
        if not image_obj:
            return HttpResponse("请上传图片")
        date=timezone.now()
        img_name = image_obj.name
        # 因为项目目录设置的不合理；理论上static应该在外层的
        img_path_save = 'static/images-article/' + str(login_No) + "_" + img_name #数据库存储的地址，用在前端展示的相对地址；是img_path的子路径
        img_path = "firstapp/" + img_path_save #用户本地存储的
        with open(img_path, "wb") as f:
            for chunk in image_obj.chunks():
                f.write(chunk)
        a=Article(articleNo=articleNo,authorNo=login_No,headline=headline,content=content,image=img_path_save,
        article_type=article_type,date=date)######有做修改
        a.save()
        return HttpResponse("发布成功！")
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User#######新加的
    article_page = render(request, 'article.html',context)#####新加的
    return article_page

def identification2(request):
    context={}
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    if request.method == 'POST':
        name=request.POST.get('name',"")
        ID_number=request.POST.get('ID_number',"")
        sex=request.POST.get('sex',"")
       # salary=request.POST.get('salary',"")
        pet_type=request.POST.get('pet_type',"")
       # service_type=request.POST.get('service_type',"")
        district=request.POST.get('district',"")
        interview_time=request.POST.get('interview_time',"")
        intro=request.POST.get('intro',"")
        k=Keeper.objects.count()+1

        head_img=request.FILES.get("evidence","")
        img =Image.open(head_img)
        img_name = str(head_img).replace("/", "_")
        img_path = "static/keeper_photo/" + str(login_No) + "_" + img_name
        img.save(img_path)# 用于保存到数据库的地址，为了调用做出改动
        img_path_save = "static/keeper_photo/" + str(login_No) + "_" + img_name

        k=Keeper(keeperNo=k,realNo=login_No,name=name,sex=sex,photo=head_img,intro=intro,ID_number=ID_number,
        interview_time=interview_time,pet_type=pet_type,star='3',city='上海',district=district)
        k.save()
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User#######新加的
    identification2_page = render(request, 'iden2.html',context)####
    return identification2_page

def chatroom(request, u_id, f_id):
    # u_id = request.user.id
    try:
        friend_obj = User.objects.get(No=f_id)
    except:
        return HttpResponse("%s is not correct id. please register it"% f_id)
    try:
        user_obj = User.objects.get(No=u_id)
    except:
        return HttpResponse("%s is not correct id. please register it"% u_id)
    history_read_obj = Chat.objects.filter(Q(senderNo=f_id, receiverNo=u_id, is_read=True)|Q(senderNo=u_id, receiverNo=f_id))
    history_unread_obj = Chat.objects.filter(receiverNo=u_id, senderNo=f_id, is_read=False)

    history_msg = history_read_obj.order_by('-create_time')[0:10][::-1]
    history_unread_msg = list(history_unread_obj.all())

    # process time: to do use timezone
    # +8小时是真正的北京时间
    for m in history_msg:
        create_time = m.create_time
        create_time = create_time + timedelta(hours=8)
        m.create_time = create_time

    for m in history_unread_msg:
        create_time = m.create_time
        create_time = create_time + timedelta(hours=8)
        m.create_time = create_time
    login_No=request.session.get('login_No','')#########新加的
    login_User=User.objects.filter(No=login_No)######新加的
    history_unread_obj.update(is_read=True)
    return render(request, 'chatfriend.html', {'history_msg':history_msg, 'history_unread_msg':history_unread_msg, 'f_obj':friend_obj, 'u_obj':user_obj,'login_No':login_No,'login_User':login_User})

def pmess(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    context['login_No']=login_No#######新加的
    login_User=User.objects.filter(No=login_No)######新加的
    context['login_User']=login_User######新加的
    Chat_list=Chat.objects.all()
    User_list=User.objects.all()
    context['Chat_list']=Chat_list
    context['User_list']=User_list
    if request.method == 'POST':
        head_img=request.FILES.get("img","")
        img =Image.open(head_img)
        img_name = str(head_img).replace("/", "_")
        img_path = "static/user_img/" + str(login_No) + "_" + img_name
        img.save(img_path)# 用于保存到数据库的地址，为了调用做出改动
        img_path_save = "static/user_img/" + str(login_No) + "_" + img_name
        User.objects.filter(No=login_No).update(image=img_path_save)   
    pmess_page = render(request, 'pmess.html',context)####新加
    return pmess_page

def pingjia(request):
    context={}####新加
    login_No=request.session.get('login_No','')#########新加的
    keeperNo=request.session.get('keeperNo','')
    orderNo=request.GET['orderNo']
    request.session['orderNo']=orderNo

    date=timezone.now()
    if request.method == 'POST':
        score=int(request.POST.get('score',""))
        comment=request.POST.get('comment',"")
        c=ServiceComment(customerNo=login_No,keeperNo=keeperNo,orderNo=orderNo,score=score,co_time=date,comment=comment)
        c.save()
        #Order.objects.filter(ordNo=orderNo).update(state="已完成")    
        #keeper评分

    context['login_No']=login_No#######新加的
    context['keeperNo']=keeperNo#######新加的
    context['orderNo']=orderNo#######新加的
    return render(request, "pingjia.html",context)####新加



@csrf_exempt
def digg(request):
    article_id = request.POST.get("article_id", "")
    article = Article.objects.filter(articleNo=article_id)
    digg_type = request.POST.get("digg_type", "up")
    if digg_type == "up":
        article.update(likes=F('likes')+1)
    else:
        article.update(likes=F('likes')-1)
    return HttpResponse("OK")