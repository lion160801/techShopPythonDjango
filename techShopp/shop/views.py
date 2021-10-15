#mấy cái này không biết
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import  check_password
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import  HttpResponseRedirect

#những view cần thiết để hiển thị
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views import View
#Model để truyền các object
from .models import *


def recentlyCus(request):
    cus = Customer
    if request.session.get('customer'):
        cusid = request.session.get('customer')
        cus = Customer.get_customer_by_cusid(cusid)
    print(cus.name)
    return cus


# Trang chủ
class Index(TemplateView):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        product_list = None
        pg_list = PGroup.get_all_pg()
        PGID = request.GET.get('pgroup')
        if PGID:
            product_list = Product.get_all_products_by_pgid(PGID)
            print(PGID)
        else:
            product_list = Product.get_all_products_by_pgid(8)
        context = {'product_list': product_list, 'pg_list': pg_list,'cus':recentlyCus(request)}
        return render(request, 'shop/index.html', context)


# Trang chi tiết sản phẩm
class Product_Detail(View):
    def post(self, request, p_id):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        # request.session['cart'].clear()
        print('cart', request.session['cart'])
        return redirect('cart')

    def get(self, request, p_id):
        product = Product.objects.get(pk=p_id)
        print('Sản phẩm:', product)
        context ={'product': product,'cus':recentlyCus(request)}
        return render(request, 'shop/product-detail.html',context)


# Trang chi tiết sản phẩm
class Order_Detail(View):
    def get(self, request, p_id):
        order = Product.objects.get
        print('Sản phẩm:', order)
        context ={'order': order}
        return render(request, 'shop/product-detail.html',context)

#Trang đơn hàng
class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        context = {'products' : products,'cus':recentlyCus(request)}
        return render(request , 'shop/cart.html' , context)

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        for product in products:
            print(cart.get(str(product.pro_id)))
            order = Order(customer=Customer(cus_id=customer),
                          product=product,
                          price=product.pro_price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.pro_id)))
            order.save()
        request.session['cart'] = {}
        return render(request, 'shop/success.html')

# Trang đăng nhập
class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'shop/login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.cus_id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('index')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'shop/login.html', {'error': error_message})
#Đăng xuất
def Logout(request):
    request.session.clear()
    return redirect('login')

#Trang đăng kí
class Register(View):
    def get(self, request):
        return render(request, 'shop/register.html')
    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        address = postData.get('address')
        mobile = postData.get('mobile')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'name': name, 'address': address, 'mobile': mobile,'email': email
        }
        error_message = None
        customer = Customer(name=name,
                            address=address,
                            mobile=mobile,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)
        if not error_message:
            print(name, address, mobile, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return render(request, 'shop/successregister.html')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'shop/register.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.name):
            error_message = "First Name Required !!"
        elif len(customer.name) < 1:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.address:
            error_message = 'Last Name Required'
        elif len(customer.address) < 1:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.mobile:
            error_message = 'Phone Number required'
        elif len(customer.mobile) < 1:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 1:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 1:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

#Trang kết quả tìm kiếm
class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        Psearch_list = Product.objects.filter(
            Q(pro_name__icontains=query) | Q(brand__name__icontains=query)
        )
        return Psearch_list

def detail(request):
    cus = recentlyCus(request)
    order = Order.objects.all().filter( customer = cus)
    return render(request, 'shop/detail.html', {'order': order})