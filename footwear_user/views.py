from django.shortcuts import render,redirect
from .models import *
import random
import requests
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'
# Create your views here.
########################################### User Side #################################################
def index(request):
	try:
		products=Product.objects.filter()
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="buyer":
			return render(request,'index.html',{'products':products})
		else:
			return redirect('seller-index')
	except:
		return render(request,'index.html',{'products':products})

def contact(request):
	if request.method=='POST':
		try:
			Contact.objects.get(email=request.POST['email'])
			msg=" Alredy Exist"
			return render(request,'contact.html',{'msg':msg})
		except:
			Contact.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					sub=request.POST['sub'],
					message=request.POST['message']
				)
			msg="Send Successfully"
			return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def about(request):
	return render(request,'about.html')

def women(request):
	products=Product.objects.filter(product_category="Female")
	return render(request,'women.html',{'products':products})

def men(request):
	products=Product.objects.filter(product_category="Male")
	return render(request,'men.html',{'products':products})


def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(
		user=user,
		product=product

	)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlists=Wishlist.objects.get(user=user,product=product)
	wishlists.delete()
	return redirect('wishlist')

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		user=user,
		product=product,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price

	)
	return redirect('cart')

def change_qty(request):
	pk=int(request.POST['pk'])
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(cart)
	for i in cart:
		net_price=net_price+i.total_price
	return render(request,'cart.html',{'cart':cart,'net_price':net_price})


def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product,payment_status=False)
	cart.delete()
	return redirect('cart')

def my_orders(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'my-orders.html',{'carts':carts})


def product_detail(request):
	products=Product.objects.all()
	user=User.objects.get(email=request.session['email'])
	return render(request,'product-detail.html',{'products':products})

def singel_product_detail(request,pk):
	wishlist_flag=False
	cart_flag=False
	products=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		Wishlist.objects.get(user=user,product=products)	
		wishlist_flag=True
	except Exception as e:
		print(e)
		pass
	try:
		Cart.objects.get(user=user,product=products,payment_status=False)
		cart_flag=True
	except Exception as e:
		print(e)
		pass
	return render(request,'singel-product-detail.html',{'products':products,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})

def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
		
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def checkout(request):
	return render(request,'checkout.html')

def order_complete(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'order-complete.html',{'carts':carts})
	

def singup(request):
	if request.method=='POST':
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Alredy Exist"
			return render(request,'singup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				if request.POST['usertype']=="buyer":
					admin_access=True
				else:
					admin_access=False
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						email=request.POST['email'],
						password=request.POST['password'],
						profile_pic=request.FILES['profile_pic'],
						usertype=request.POST['usertype'],
						admin_access=admin_access
					)
				msg="User Sing Up Successfully"
				return render(request,'singin.html',{'msg':msg})
			else:
				msg="Password Not Match"
				return render(request,'singup.html',{'msg':msg})
	else:
		return render(request,'singup.html')

def singin(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="buyer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return redirect('index')
				else:
					if user.admin_access==True:
						request.session['email']=user.email
						request.session['fname']=user.fname
						request.session['profile_pic']=user.profile_pic.url
						return redirect('seller-index')
					else:
						msg="Your admin access in still not approved, please contect admin"
						return render(request,'singin.html',{'msg':msg})
			else:
				msg="Incorrect password"
				return render(request,'singin.html',{'msg':msg})
		except Exception as e:
			print(e)
			msg="Email not registered"
			return render(request,'singin.html',{'msg':msg})
	else:
		return render(request,'singin.html')

def singout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return redirect('index')
	except:
		return redirect('index')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url
		msg="profile Updated successfully"
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})


def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('singout')
			else:
				msg="password Not matched"
				return render(request,'change-password.html',{'msg':msg})
		else:
			msg="Old password Not matched"
			return render(request,'change-password.html',{'msg':msg})
	else:
 		return render(request,'change-password.html')

def forgot_password(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OPT For forget_password'
			message = 'Hello '+user.fname+"your opt for forgot_password is: "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html' ,{'email':user.email,'otp':otp})
		except Exception as e:
			print(e)
			msg="Email Not registered"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'new-password.html',{'email':email})
	else:
		msg="Incorrect otp"
		return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})

		
def new_password(request):
	email=request.POST['email']
	np=request.POST['new-password']
	cnp=request.POST['cnew-password']

	if np==cnp:
		user=User.objects.get(email=email)
		user.password=np
		user.save()
		msg="password update successfully"
		return render(request,'singin.html',{'msg':msg})
	else:
		msg="password not match"
		return render(request,'new-password.html',{'email':email,'msg':msg})



###################################### Seller Side ###################################################

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('singout')
			else:
				msg="password Not matched"
				return render(request,'seller-change-password.html',{'msg':msg})
		else:
			msg="Old password Not matched"
			return render(request,'seller-change-password.html',{'msg':msg})
	else:
 		return render(request,'seller-change-password.html')


def seller_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url
		msg="profile Updated successfully"
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})

def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
				seller=seller,
				product_category=request.POST['product_category'],
				product_name=request.POST['product_name'],
				product_price=request.POST['product_price'],
				product_desc=request.POST['product_desc'],
				product_image=request.FILES['product_image'],
			)
		msg="Product Added Successfully"
		return render(request,'seller-add-product.html',{'msg':msg})
	else:
		return render(request,'seller-add-product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-view-product.html',{'products':products})

def seller_view_male(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Male")
	return render(request,'seller-view-product.html',{'products':products})

def seller_view_female(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Female")
	return render(request,'seller-view-product.html',{'products':products})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg="Product Updated successfully"
		return render(request,'seller-edit-product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'product':product})


def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')

def seller_index(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-index.html',{'products':products})

def seller_product_detail(request,pk):
	products=Product.objects.get(pk=pk)
	return render(request,'seller-product-detail.html',{'products':products})