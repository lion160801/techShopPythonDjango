from django.contrib import admin
from.models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pro_name','group','pro_price')  #lựa chọn phương thức hiển thị trên trang admin
    search_fields = ('pro_name', )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','email')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','product')
    search_fields = ('customer',)

admin.site.register(Product,ProductAdmin)  # đăng kí class lên trên trang admin để dễ quản lý
admin.site.register(PGroup)
admin.site.register(Brand)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer,CustomerAdmin)






