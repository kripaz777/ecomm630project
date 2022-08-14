from django.shortcuts import render
from django.views.generic import View
from .models import *

# Create your views here.
class Base(View):
	context = {}
	context['categories'] = Category.objects.all()
	context['subcategories'] = SubCategory.objects.all()
	context['brands'] = Brand.objects.all()

	all_brand = []
	for i in Brand.objects.all():
		ids = Brand.objects.get(name = i).id
		count = Product.objects.filter(brand = ids).count()
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
		return render(request,'product-detail.html',self.context)