from django.contrib import admin

from firstapp.models import Article, Comment, Keeper,Salary, Order, User,ServiceComment,Chat

# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Keeper)
admin.site.register(Order)
admin.site.register(Salary)
admin.site.register(ServiceComment)
admin.site.register(Chat)
