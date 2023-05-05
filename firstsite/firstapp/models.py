from django.db import models

class User(models.Model):
    No=models.IntegerField(primary_key=True)#编号
    ID=models.CharField(unique=True, max_length=20)
    code=models.CharField(max_length=16)               
    email=models.CharField(null=True,max_length=30)
    phone_number=models.CharField(null=True,blank=True,max_length=11)#前端注册是有手机号的
    image=models.ImageField(upload_to="static/user_img", null=True,blank=True)
    ITYPE=(
        (0,'否'),
        (1,'是')
    )
    keeper_if=models.IntegerField(choices=ITYPE,default=0)
    def __str__(self):
        return self.ID

class Keeper(models.Model):
    keeperNo=models.IntegerField(primary_key=True)#饲养员编号
 #  user=models.ForeignKey('User',on_delete=models.CASCADE)
    realNo=models.IntegerField(unique=True)
    name=models.CharField(max_length=10)#真实姓名
    SEX=(('女','女'),('男','男'))
    sex=models.CharField(max_length=2,choices=SEX)
    photo=models.ImageField(upload_to="static/keeper_photo",blank=True,null=True)#照片
    intro=models.TextField(null=True)#自我简介
    ID_number=models.CharField(max_length=18,default="31022619991229526")
    interview_time=models.CharField(max_length=6,null=True,blank=True)#面试时间----针对前端选项
    DISTRICT=(('黄浦区','黄浦区'),('徐汇区','徐汇区'),('长宁区','长宁区'),('静安区','静安区'),('普陀区','普陀区'),('虹口区','虹口区'),('杨浦区','杨浦区'),('闵行区','闵行区'),('宝山区','宝山区'),('嘉定区','嘉定区'),('金山区','金山区'),('松江区','松江区'),('青浦区','青浦区'),('奉贤区','奉贤区'),('崇明区','崇明区'),('浦东新区','浦东新区'))
    pet_type=models.CharField(max_length=10)
    star=models.FloatField(default=3)
    city=models.CharField(default='上海',max_length=2)
    district=models.CharField(max_length=4,choices=DISTRICT)
    start_time=models.DateField(null=True, blank=True, max_length=500)
    end_time=models.DateField(null=True, blank=True, max_length=500)
    def __str__(self):
        return self.name

class Salary(models.Model):
    Ser_type=(('遛狗','遛狗'),('寄养','寄养'),('上门照看','上门照看'),('看房子','看房子'))
        #    keeper=models.ForeignKey('Keeper',on_delete=models.CASCADE)
    keeperNo=models.IntegerField()
    service_type=models.CharField(choices=Ser_type,max_length=4)
    salary=models.IntegerField(null=True)
    '''class Meta:
        db_table = 'firstapp_salary'
        unique_together = ("keeperNo", "service_type")'''
    def __str__(self):
        return str(self.service_type)

class Article(models.Model):
  #  user=models.ForeignKey('User',on_delete=models.CASCADE)   
    articleNo=models.IntegerField(primary_key=True)#文章编号
    authorNo=models.IntegerField()#限制条件：？
    headline = models.CharField(max_length=20)
    content = models.TextField(null=True)
    TYPE=(
        ('爱宠故事','爱宠故事'),
        ('科普知识','科普知识'),
        ("交流讨论","交流讨论"),
    )
    image = models.ImageField(upload_to='static/article_image',null=True)
    article_type=models.CharField(null=True, blank=True, max_length=10,choices=TYPE)
    date=models.DateField(null=True)
    views=models.IntegerField(null=True,default=0)
    likes=models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.headline

class Comment(models.Model):
  #  user=models.ForeignKey('User',on_delete=models.CASCADE)
  #  article=models.ForeignKey('Article',on_delete=models.CASCADE)
    articleNo=models.IntegerField(default=1)
    time=models.DateField(null=True)
    userNo=models.IntegerField(null=True)
    text=models.TextField(max_length=200)
    '''class Meta:
        db_table = 'firstapp_comment'
        unique_together = ("articleNo", "time")'''
    def __str__(self):
        return str(self.articleNo)

class Order(models.Model):#订单编号=开始时间+地区(数字表示)+饲养员编号+orderNo
    STATE_CHOICES = (
        ('已完成', '已完成'),
        ('正在进行', '正在进行')
    )
  #  user=models.ForeignKey('User',on_delete=models.CASCADE)
  #  keeper=models.ForeignKey('Keeper',on_delete=models.CASCADE)
    orderNo=models.IntegerField(primary_key=True)#订单编号
    customerNo=models.IntegerField()#用户编号
    keeperNo=models.IntegerField()
    start_time=models.DateField()
    end_time=models.DateField()
    money=models.IntegerField()
    address=models.CharField(null=True,blank=True,max_length=100)
    state=models.CharField(choices=STATE_CHOICES, default=0,max_length=4)#订单状态
    def __str__(self):
        return str(self.orderNo)

class ServiceComment(models.Model):
  #  user=models.ForeignKey('User',on_delete=models.CASCADE)
  #  keeper=models.ForeignKey('Keeper',on_delete=models.CASCADE)
  #  order=models.ForeignKey('Order',on_delete=models.CASCADE)
    orderNo=models.IntegerField()
    customerNo=models.IntegerField()#用户编号
    keeperNo=models.IntegerField()
    score=models.IntegerField(blank=True,null=True)
    comment=models.CharField(blank=True,null=True,max_length=200)#评价
    co_time=models.DateField()#时间
    def __str__(self):
        return str(self.orderNo)

class Chat(models.Model):
 #   user=models.ForeignKey('User',on_delete=models.CASCADE)
  #  keeper=models.ForeignKey('Keeper',on_delete=models.CASCADE)
    senderNo=models.IntegerField()
    receiverNo=models.IntegerField()
    create_time=models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    text=models.TextField(max_length=1024,blank=True,null=True)
    image=models.ImageField(upload_to="static/chat_img",blank=True,null=True)
    video=models.FileField(upload_to="static/chat_media",blank=True,null=True)
    is_read=models.BooleanField(default=False, verbose_name='是否已读')
    '''class Meta:
        db_table = 'firstapp_chat'
        unique_together = ("senderNo", "receiverNo","time")'''
