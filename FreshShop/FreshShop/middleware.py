import os
import datetime
from FreshShop.settings import BASE_DIR

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


# class MiddlewearTest(MiddlewareMixin):
#     def process_request(self, request):
#         """
#         :param request:视图没有处理的请求
#         :return:
#         """
#         username = request.Get("username")
#         if username and username == "abc":
#             return HttpResponse("404")

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     """
    #     :param request: 视图没有处理的请求
    #     :param view_func: 视图函数
    #     :param view_args: 视图函数的参数，元组格式
    #     :param view_kwargs: 视图函数的参数，字典格式
    #     :return:
    #     """
    #     print(view_func(request, view_args))
    #
    # def process_exception(self, request, exception):
    #     """
    #
    #     :param request: 视图处理中的函数
    #     :param exception: 错误
    #     :return:
    #     """
    #     now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     level="Error"
    #     content=str(exception)
    #     log_result="%s [%s] %s \n"%(now,level,content)
    #     file_path=os.path.join(BASE_DIR,"error/log",)
    #     with open(file_path,"a")as f :
    #         f.write(log_result)
    #     print(exception)
    # def process_templates_response(self, request):
    #     return ("process_templates_response")
    #
    # def process_response(self, request,response):
    #     response.set_cookie("hhh","111")
    #     return response
