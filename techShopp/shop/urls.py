
from django.urls import path
from .views import *
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('detail<int:p_id>/', Product_Detail.as_view(), name='Pdetail'),  #Trang chi tiết sản phẩm
    path('', Index.as_view(), name='index'), #Trang chủ
    path('search/', SearchResultsView.as_view(), name='search_results'), #Trang kết quả tìm kiếm
    path('login', Login.as_view(), name='login'), #Trang đăng nhập
    path('logout', Logout, name='logout'), #Đăng xuất
    path('register', Register.as_view(), name='register'), #Trang đăng kí
    path('cart', auth_middleware(Cart.as_view()), name='cart'),#Trang giỏ hàng

]
