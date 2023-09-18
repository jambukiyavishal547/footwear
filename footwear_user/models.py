from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	email=models.EmailField()
	password=models.CharField(max_length=30)
	profile_pic=models.ImageField(upload_to="profile_pic/",default="")
	usertype=models.CharField(max_length=100,default="buyer")
	admin_access=models.BooleanField(default=False)

	def __str__(self):
		return self.fname+" "+self.lname

class Contact(models.Model):
	fname=models.CharField(max_length=50)
	lname=models.CharField(max_length=50)
	email=models.EmailField()
	sub=models.CharField(max_length=100)
	message=models.TextField()

	def __str__(self):
		return self.fname+" "+self.lname

		
class Product(models.Model):
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	choice1=(
		("Male","Male"),
		("Female","Female"),
	)
	product_category=models.CharField(max_length=200,choices=choice1,default="Male")
	product_name=models.CharField(max_length=100)
	product_price=models.PositiveIntegerField()
	product_desc=models.TextField()
	product_image=models.ImageField(upload_to='product_image')

	def __str__(self):
		return self.seller.fname+" - "+self.product_name


class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.fname+ " - "+ self.product.product_name
		

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	product_price=models.PositiveIntegerField()
	product_qty=models.PositiveIntegerField(default=1)
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)

	def __str__(self):
		return self.user.fname+ " - "+ self.product.product_name


