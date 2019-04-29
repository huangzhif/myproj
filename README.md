# myproj
# 一、环境准备
1、[环境配置](https://www.jianshu.com/p/2071e85945c2 "悬停显示")  
2、进入opt目录 并执行命令
   ```angular2html
   git clone https://github.com/huangzhif/myproj.git
   
   # 安装包
   pip install -r requirements.txt
   
   # 修改 /myproj/settings.py 中的数据库配置
   python manage.py migrate
   python manage.py createsuperuser
   
   # 运行
   python manage.py runserver 0.0.0.0:8000
```