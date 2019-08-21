import time
from django.db.models import Sum
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from Buyer.models import *
from Store.views import set_password
from Store.models import *

from alipay import AliPay
# Create your views here.
# def base(request):
#     return render(request,"buyer/base.html")
def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Store/login")

    return inner###
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                if web_password == user.password:
                    response = HttpResponseRedirect("/Store/index/")
                    response.set_cookie("username", username)
                    request.session["username"] = user.username
                    response.set_cookie("user_id", user.id)
                    return response
    return render(request, "buyer/login.html")
def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect("/Store/login/")
    return render(request, "buyer/register.html")
@loginValid
def index(request):
    #空列表用来存放类型的信息以及前端要展示的数据
    result_list = []
    #查询所有商品类型
    goods_type_list = GoodsType.objects.all()
    for goods_type in goods_type_list:
        #查询出每个类型的前四条商品数据，作为前端商品数据的展示
        good_list = goods_type.goods_set.values()[:4]
        print(good_list)
        if good_list:
            goodsType = {
                "id": goods_type.id,
                "name": goods_type.name,
                "description": goods_type.description,
                "picture": goods_type.picture,
                "goods_list": good_list
            }
            result_list.append(goodsType)
    return render(request, "buyer/index.html", locals())
def logout(request):
    response = HttpResponseRedirect("/Store/login")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response
@loginValid
def good_list(request):
    '''
    商品列表页的数据展示，显示对应类型的商品列表信息
    '''
    good_list = []
    #通过前端点击查看更多，传入该商品类型的id，type_id参数通过get方式传递到view
    type_id = request.GET.get("type_id")
    #通过传入的type_id来查询该类型对象
    goods_type = GoodsType.objects.filter(id=type_id).first()
    #如果存在
    if goods_type:
        #通过反向查询出该类型的所有的商品，且查询出的结果必须为上架的商品
        goodsList = goods_type.goods_set.filter(goods_under=1)
        #将查询结果通过locals()传递到goos_list.html供其做前端数据渲染
    return render(request, "buyer/goods_list.html", locals())
def pay_result(request):
    return render(request, "buyer/pay_result.html", locals())
def pay_order(request):
    money = request.GET.get("money")
    order_id = request.GET.get("order_id")
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoczMn0f7kzCDGopTDH7T6VtvroeGugJRNeCMKF2MLFx9GlspQqqo978dXrtPKef5LEI2emiu/0Qv8WVKZ2hvg1bzZWpv2n7SMp7dtkaJ5tcpHJj974KvvgtZu/hZahLAMUbvlvpHxMIRdqddKvSSrhmiAcFxVkfJuXiw7XGKikx/RPR3dOPiP5rSjba4pZZ1k/aFizHNnrVEztHxU5vR2pMRmZwLv5NHMRPOj3f4r3OZeiEHQTj8QWgx0MxD8zrYucUfQ8QZOSS+mqKhJjWs1Ezs6RZnFw/ZnnDR1623roNU6IIYAYE9K0h6FYbIEcAouyGhuoWAZhi8bwH6/u6ZIwIDAQAB
    -----END PUBLIC KEY-----"""
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChzMyfR/uTMIMailMMftPpW2+uh4a6AlE14IwoXYwsXH0aWylCqqj3vx1eu08p5/ksQjZ6aK7/RC/xZUpnaG+DVvNlam/aftIynt22Ronm1ykcmP3vgq++C1m7+FlqEsAxRu+W+kfEwhF2p10q9JKuGaIBwXFWR8m5eLDtcYqKTH9E9Hd04+I/mtKNtrillnWT9oWLMc2etUTO0fFTm9HakxGZnAu/k0cxE86Pd/ivc5l6IQdBOPxBaDHQzEPzOti5xR9DxBk5JL6aoqEmNazUTOzpFmcXD9mecNHXrbeug1ToghgBgT0rSHoVhsgRwCi7IaG6hYBmGLxvAfr+7pkjAgMBAAECggEAPB+fNd0IxgQz44vdGnqSgleA46jmzn4H8W5UhrdkXCOuNToE1goWqaEx577QxvC1bdXY6pm11ZNgAWKzSEPNlE+eOGRZ1iZkM31HQ/FoUwhG9aKAUh0M8yDCoo/BoiH/mxAR/ddZDetTk/TTMSAa1WkfA2n/lKEue6Y2kLUtVwBGHUUszrpZtmB0rbl3uVm4TzoCRUJF5sTMMU48pU0H8LfEAdsQnwP8YvBxznJDBrK79O/VHAupi1EosC1bNs71GPCiBjmim72AJzpTWZRoMdSlFM/KFkAxqcQpFy34w8z0BSusnSVDdbTia2uIYETYqfqRfrdY/nos6mdblejF0QKBgQD18J6Pre3Pxj6mIverW0PlL3YP//wf/CZV9NACduAniXl3eYK92gWnmID2so3ADa3Ds5B8ViHrBdq1ov/0vrKr98Q79oKfQVGitU2xVzXOaFGaA+CtUIIHbUTvml37mkyNwqjvPTjP0h4puPj4E5ZxJib3h9bHArSz4go0AvQUiwKBgQCoaxoEdIDGKNCgHFiLT4rWr+7UmfkwsuWwe4VNfG+AwTmCTx5VpKqchvprz4r6IK/z3VYAI7Xd3vc0aNq08Gl7CsqwKYIC/RxugJxcLacODKZNonBMxpUja0tebOC6Xi4DQ9T06aTf0Hk0nfXfmERtz2nIYra3ZI5Jp/3SYxZoyQKBgQDNJ9xNBIylTr0B/5dUZPxdGVtF+4bI86DTATXnaFyR/pbJuB382vrulEO4BrhCJeb2ojp7zanbkHWiIQeclNscosEaOAc8a9N6g/z8W0ByHwk7DdMFIGxnX5oquT1+3XbQpjof35Udnyw0J63f2w8a8fV9dN4QAszUZVGXk4MiAwKBgGpcGPYvTRPXuskinZh9B0VFniKNip2CnSOzHiAtMY2yeUseBB45+7UWWRe03iPQeM4dPa6g3r3bjWp/vX7/RN37lr1huUWB626tshFUk2d//ZaRuzIBRzYzEEn1oIaR66UMNXTmCMV/tsvP5fLrCmv+zONL0/BFhMZnXRh8ky5hAoGAKV5CHHb0kBspiJodcdz+L+vGlJ/limwi5eBNF7KmkXS9SbW2A6HMNwIJZOJvMTw39nxOf/Kc+W+EWcWVvUYa+xF1um0vMu1Tx3b35I4ooywK8H72nMWJZm0H/pNFe0ElWvwbenReC3bzjOIJZ0S1DKTd9fVMGXhBd7f/W/3sUsw=
    -----END RSA PRIVATE KEY-----"""

    # 实例化支付应用
    alipay = AliPay(
        appid="2016101000652501",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )
    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),
        subject="生鲜交易",
        return_url="http://127.0.0.1:8000/Store/pay_result/",
        notify_url="http://127.0.0.1:8000/Store/pay_result/"
    )
    order=Order.objects.get(order_id=order_id)
    order.order_status=2
    order.save()
    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)
def user_order(request):
    return render(request,"buyer/user_center_order.html")
def user_site(request):
    user_id = request.COOKIES.get("user_id")
    address_list = Address.objects.filter(buyer_id_id=user_id)
    if request.method=="POST":
        recver=request.POST.get("recver")
        addresss=request.POST.get("addresss")
        recver_number=request.POST.get("recver_number")
        user_id=request.COOKIES.get("user_id")
        recver_phone=request.POST.get("recver_phone")
        address=Address()
        address.address=addresss
        address.recver=recver
        address.recver_number=recver_number
        address.recver_phone = recver_phone
        address.buyer_id=Buyer.objects.get(id=int(user_id))
        address.save()
    return render(request,"buyer/user_center_site.html",locals())
def user_info(request):
    user_id=request.COOKIES.get("user_id")
    buyer=Buyer.objects.get(id=user_id)
    return render(request,"buyer/user_center_info.html",locals())
def detail(request):
    # '''
    #    商品列表页的数据展示，显示对应类型的商品列表信息
    #    '''
    # good_list =Goods.objects.all()
    # # 通过前端点击查看更多，传入该商品类型的id，type_id参数通过get方式传递到view
    # id = request.GET.get("id")
    # # 通过传入的type_id来查询该类型对象
    # Store = Goods.objects.filter(id=id).first()
    #
    # return render(request,"buyer/detail.html",locals())
    id = request.GET.get("id")
    if id:
        goods=Goods.objects.filter(id=id).first()
        if goods:
            return render(request,"buyer/detail.html",locals())
    return HttpResponseRedirect("没有指定的商品")
def setOrder(user_id,goods_id,store_id):
    #格式化订单编号
    strtime=time.strftime("%Y%m%d%H%M%S",time.localtime())
    order_id=strtime+str(user_id)+str(goods_id)
    return order_id
def place_order(request):
    user_id=request.COOKIES.get("user_id")
    address_list=Address.objects.filter(buyer_id_id=user_id)
    if request.method=="POST":
        count=int(request.POST.get("count"))
        goods_id=request.POST.get("goods_id")
        user_id=request.COOKIES.get("user_id")
        goods=Goods.objects.get(id=goods_id)
        store_id=goods.store_id.id #*******
        price=goods.goods_price
        order=Order()
        order.order_id=setOrder(str(user_id),str(goods_id),str(store_id))
        order.goods_count=count
        order.order_user=Buyer.objects.get(id=user_id)
        order.order_price=count*price
        order.save()
        order_detail=OrderDetail()
        order_detail.order_id=order#******
        order_detail.goods_id=goods_id
        order_detail.goods_name=goods.goods_name
        order_detail.goods_price=goods.goods_price
        order_detail.goods_number=count
        order_detail.goods_total=count*goods.goods_price
        order_detail.goods_store=store_id
        order_detail.goods_image=goods.goods_image
        order_detail.save()

        detail=[order_detail]
        return render(request,"buyer/place_order.html",locals())
    else:
        order_id=request.GET.get("order_id")
        if order_id:
            order=Order.objects.get(id=order_id)
            detail=order.orderdetail_set.all()
            return render(request,"buyer/place_order.html",locals())
        else:
            return HttpResponse("非法请求")
def cart(request):
    user_id=request.COOKIES.get("user_id")
    goods_list=Cart.objects.filter(user_id=user_id)
    goods_pricetotal = sum([int(i.goods_price) for i in goods_list])
    goods_numbers=[]
    for x in goods_list:
        goods_numbers.append(x.goods_number)
    goods_number=len(goods_numbers)
    if request.method=="POST":
        post_data=request.POST
        print(post_data)
        cart_data=[]#收集从前端传递过来的商品
        for k,v in post_data.items():
            if k.startswith("goods_"):
                cart_data.append(Cart.objects.get(id = int(v)))
        goods_count=len(cart_data)#提交过来的数据总的数量
        #订单总价
        goods_total=sum([int(i.goods_total)for i in cart_data])
        # #修改使用聚类查询返回指定商品的总价
        # 1.查询到所有商品
        # cart_data=[]#收集前端传递过来的商品id
        # for k,v in post_data.items():
        #     if k.startswith("goods_"):
        #         cart_data.append(int(v))
        #         #使用in方法进行范围划定，然后使用sum方法进行计算
        # cart_goods=Cart.objects.filter(id__in=cart_data).aggregate(Sum("goods_total"))
        # print(cart_goods)
        #保存订单
        order=Order()
        #订单中有多个商品或多个店铺使用goods_count来代替商品id,用2代替店铺id
        order.order_id=setOrder(user_id,goods_count,"2")
        order.goods_count=goods_count
        order.order_user=Buyer.objects.get(id=user_id)
        order.order_price=int(goods_total)
        order.order_status=1
        order.save()
        #保存订单详情
        #这里的detail是购物车里的数据实例，不是商品实例
        for detail in cart_data:
            order_detail=OrderDetail()
            order_detail.order_id=order
            order_detail.goods_id=detail.goods_id
            order_detail.goods_name=detail.goods_name
            order_detail.goods_price=detail.goods_price
            order_detail.goods_number=detail.goods_number
            order_detail.goods_total=detail.goods_total
            order_detail.goods_store=detail.goods_store
            order_detail.goods_image=detail.goods_picture
            order_detail.save()
            #order 是一条订单支付页
        url="/Store/place_order/?order_id=%s"%order.id
        return HttpResponseRedirect(url)
    return render(request,"buyer/cart.html",locals())
def add_cart(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        goods = Goods.objects.get(id=int(goods_id))
        user_id = request.COOKIES.get("user_id")
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total =goods.goods_price * count
        cart.goods_number = count
        cart.goods_picture = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.id
        cart.user_id = user_id
        cart.save()
        result["state"] = "success"
        result["data"] = "商品添加成功"
    else:
        result["data"] = "请求错误"
    return JsonResponse(result)
def user_center_order(request):
    """
    1.先获取到当前用户
    2.根据用户查到订单消息
    3.根据订单编号查询到应订单详情

    """
    orderdetail_list=[]
    userid=request.COOKIES.get("user_id")
    order=Order.objects.filter(order_user_id=userid)
    print(order)
    for i in order:
        orderdetaillist=i.orderdetail_set.all()
        orderdetail_list.append(orderdetaillist)
    return render(request,"buyer/user_center_order.html",locals())
# 列表页

# def list_view(request):























