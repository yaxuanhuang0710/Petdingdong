1.	安装python、VS code、MySQL、Memurai后，在通过pip install 文件夹中的requirements.txt，来安装相关依赖包。

2.	在VS code中打开文件夹，并在Mysql中创建名为“django”的数据库，在setting.py中第90行修改连接mysql数据库的密码。然后通过”python manage.py makemigrations”和” python manage.py migrate”来迁移数据库。之后就可以” python manage.py runserver”运行网站。

3.	初始进入网址为http://127.0.0.1:8000/main

4.	数据库中数据可以通过导入，也可自己创建数据进行尝试。（通过” python manage.py createsuperuser”可以创建超级用户，然后在http://127.0.0.1:8000/admin进入后台）
