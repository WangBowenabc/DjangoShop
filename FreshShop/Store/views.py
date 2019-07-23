import hashlib

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Store.models import *


def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            user = Seller.objects.filter(username=c_user).first()
            if user:
                return fun(request, *args, **kwargs)
        return HttpResponseRedirect("/Store/login/")

    return inner


def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = set_password(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect("/Store/login/")
    return render(request, "store/register.html")


def login(request):
    response = render(request, "store/login.html")
    response.set_cookie("login_from", "login_page")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                cookies = request.COOKIES.get("login_from")
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/Store/index/")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id",user.id)
                    request.session["username"] = username
                    return response
    return response


@loginValid
def index(request):
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request, "store/index.html", {"is_store": is_store})
# Create your views here.
def base(request):
    return render(request, "store/base.html")


def register_store(request):
    type_list=StoreType.objects.all()
    if request.method=="POST":
        post_data=request.POST
        store_name=post_data.get("store_name")
        store_description=post_data.get("store_description")
        store_phone=post_data.get("store_phone")
        store_money=post_data.get("store_money")
        store_address=post_data.get("store_address")
        user_id=int(request.COOKIES.get("user_id"))
        type_list=post_data.getlist("type")#获得一个列表
        store_logo=request.FILES.get("store_logo")
        store=Store()
        store.store_name=store_name
        store.store_description=store_description
        store.store_phone = store_phone
        store.store_money=store_money
        store.store_address=store_address
        store.user_id = user_id
        store.store_logo=store_logo
        store.save()
        for i in type_list:
            store_type=StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
    return render(request,"store/register_store.html",locals())
