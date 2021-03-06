from django.conf import settings
from celery import Celery
import os


#设置celery执行的环境变量，执行django项目的配置文件
os.environ.setdefault("DHANGO_SETTINGS_MODULE","CeleryTask.settings")
#创建celery应用
app=Celery('art_project')
app.config_from_object('django.conf:settings')#加载配置文件
#如果在工程的应用中创建了task.py模块，那么Celery应用就会自动去检索创建的任务，比如你添加了一个任务
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
