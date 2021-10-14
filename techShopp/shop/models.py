
from django.db import models
import datetime

#Nhóm sản phẩm
class PGroup(models.Model):
    name = models.CharField(max_length=255)

    @staticmethod
    def get_all_pg():  #Để lấy tất cả nhóm sản phẩm
        return PGroup.objects.all()

    def __str__(self): #Hiển thị tên nhóm sản phẩm
        return self.name

#Thương hiệu
class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self): #Hiển thị tên nhóm thương hiệu
        return self.name

#Sản phẩm
class Product(models.Model):
    pro_id = models.AutoField(primary_key='true')
    pro_name = models.CharField(max_length=255)
    group = models.ForeignKey(PGroup, on_delete=models.CASCADE)
    pro_price = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pro_image = models.ImageField(upload_to='shop_images')  # phải install 3rd party package: Pillow

    @staticmethod
    def get_products_by_id(ids):  #lấy sản phẩm bằng id sản phẩm
        return Product.objects.filter(pro_id__in=ids)

    @staticmethod
    def get_all_products(): #lấy tất cả sản phẩm
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_pgid(pg_id):  #Lấy danh sách sản phẩm bằng id
        if pg_id:
            return Product.objects.filter(group=pg_id)
        else:
            return Product.get_all_products();

    def __str__(self): #Hiển thị tên sản phẩm
        return self.pro_name

#Khách hàng
class Customer(models.Model):
    cus_id = models.AutoField(primary_key='true')
    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    mobile = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=200)

    def __str__(self): #Hiển thị tên khách hàng
        return self.name

    def register(self):  #đăng kí khách  hàng
        self.save()

    @staticmethod
    def get_customer_by_email(email): #lấy khách hàng bằng email
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    @staticmethod
    def get_customer_by_cusid(cus_id): #lấy khách hàng dựa vào id khách hàng
        try:
            return Customer.objects.get(cus_id=cus_id)
        except:
            return False

    def isExists(self): #kiểm tra khách hàng đã tồn tại hay chưa
        if Customer.objects.filter(email=self.email):
            return True
        return False

#Đơn hàng
class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self): #lưu lại đơn hàng
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id): #lấy đơn hàng của khách hàng cần tìm
        return Order.objects.filter(customer=customer_id).order_by('-date')

    def __str__(self): #Hiển thị tên của khách hàng đã mua sản phẩm
        return self.customer.name

