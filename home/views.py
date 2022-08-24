from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
class Base(View):
	context = {}
	context['categories'] = Category.objects.all()
	context['subcategories'] = SubCategory.objects.all()
	context['brands'] = Brand.objects.all()

	all_brand = []
	for i in Brand.objects.all():
		print(i)
		ids = Brand.objects.get(name = i).id
		count = Product.objects.filter(brand_id = ids).count()
		all_brand.append({'product_count':count,'ids':ids})
	context['counts'] = all_brand


class HomeView(Base):
	def get(self,request):
		self.context
		self.context['sliders'] = Slider.objects.all()
		self.context['ads'] = Ad.objects.all()
		self.context['hots'] = Product.objects.filter(labels = 'hot')
		self.context['news'] = Product.objects.filter(labels = 'new')
		return render(request,'index.html',self.context)

class CategoryView(Base):
	def get(self,request,slug):
		self.context
		ids = Category.objects.get(slug =slug).id
		self.context['cat_products'] = Product.objects.filter(category_id = ids)
		return render(request,'category.html',self.context)

class DetailView(Base):
	def get(self,request,slug):
		self.context
		self.context['sales'] = Product.objects.filter(labels = 'sale')
		self.context['products'] = Product.objects.filter(slug = slug)
		ids = Product.objects.get(slug =slug).subcategory_id
		self.context['subcat_products'] = Product.objects.filter(subcategory_id = ids)
		self.context['review_product'] = ProductReview.objects.filter(slug = slug)
		return render(request,'product-detail.html',self.context)


def product_review(request,slug):
	username = request.user.username
	email = request.user.email
	if request.method == 'POST':
		comment = request.POST['comment']
		star = request.POST['star']
		data = ProductReview.objects.create(
			username = username,
			email = email,
			comment = comment,
			star = star,
			slug = slug
		)
		data.save()
		return redirect(f'/detail/{slug}')
	return redirect(f'/detail/{slug}')
class SearchView(Base):
	def get(self,request):
		if request.method == 'GET':
			query = request.GET['query']
			if query is not None:
				self.context['search'] = Product.objects.filter(name__icontains = query)
			else:
				return redirect('/')

		return render(request,'search.html',self.context)


def signup(request):
	if request.method == 'POST':
		f_name = request.POST['first_name']
		l_name=request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,'The username is already taken')
				return redirect('/signup')
			elif User.objects.filter(email = email).exists():
				messages.error(request,'The emai is already taken')
				return redirect('/signup')
			else:
				user = User.objects.create(
				first_name = f_name,
				last_name = l_name,
				username = username,
				email = email,
				password = password
				)
				user.save()
		else:
			messages.error(request,'The password does not match')
			return redirect('/signup')

	return render(request,'signup.html')


class CartView(Base):
	def get(self,request):
		username = request.user.username
		self.context['my_cart'] = Cart.objects.filter(username = username,checkout = False)
		return render(request,'cart.html',self.context)

from django.contrib.auth.decorators import login_required
@login_required

def add_to_cart(request,slug):
	username = request.user.username
	if Product.objects.filter(slug = slug).exists():
		if Cart.objects.filter(slug = slug,username = username,checkout = False).exists():
			quantity= Cart.objects.get(slug = slug,username = username,checkout = False).quantity
			price = Product.objects.get(slug = slug).price
			discounted_price = Product.objects.get(slug = slug).discounted_price
			if discounted_price > 0:
				original_price = discounted_price
			else:
				original_price = price
			quantity = quantity +1
			total = original_price*quantity
			Cart.objects.filter(slug=slug, username=username, checkout=False).update(total = total,quantity = quantity)
			return redirect('/cart')
		else:
			price = Product.objects.get(slug=slug).price
			discounted_price = Product.objects.get(slug=slug).discounted_price
			if discounted_price > 0:
				original_price = discounted_price
			else:
				original_price = price

			carts = Cart.objects.create(
			username = username,
			total = original_price,
			slug = slug,
			items = Product.objects.filter(slug = slug)[0]
			)
			carts.save()
			return redirect('/cart')

def delete_product(request,slug):
	username = request.user.username
	Cart.objects.filter(slug=slug, username=username, checkout=False).delete()
	return redirect('/cart')

def reduce_product(request,slug):
	username = request.user.username
	if Cart.objects.filter(slug=slug, username=username, checkout=False).exists():
		quantity = Cart.objects.get(slug=slug, username=username, checkout=False).quantity
		price = Product.objects.filter(slug=slug).price
		discounted_price = Product.objects.filter(slug=slug).discounted_price
		if discounted_price > 0:
			original_price = discounted_price
		else:
			original_price = price
		if quantity>1:
			quantity = quantity - 1
			total = original_price * quantity
			Cart.objects.filter(slug=slug, username=username, checkout=False).update(total=total, quantity=quantity)
			return redirect('/cart')

		return redirect('/cart')


#-------------------------------------------------------------------API-----------------------------------------------
from rest_framework import  viewsets,generics
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['category', 'subcategory','brand','stock','labels']
    search_fields = ['name', 'description','specification']
    ordering_fields = ['price','id','discounted_price']

class CRUDViewSet(APIView):
	def get_object(self,pk):
		try:
			return  Product.objects.get(pk = pk)
		except:
			print('The id does not exists')

	def get(self,request,pk):
		product_data = self.get_object(pk)
		serializer = ProductSerializer(product_data)
		return Response(serializer.data)

	def post(self,request,pk):
		serializer = ProductSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"The value is posted"})

	def put(self,request,pk):
		product_data = self.get_object(pk)
		serializer = ProductSerializer(product_data,data = request.data,partial = True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response({'status':'The value is updated'})

	def delete(self,request,pk):
		try:
			Product.objects.filter(id = pk).delete()
		except:
			return Response({'status': 'The id is not in database'})
		return Response({'status': 'The value is updated'})

