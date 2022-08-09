from django.shortcuts import render
from django.views.generic import View
from .models import *

# Create your views here.
class Base(View):
	context = {}

class HomeView(Base):
	def get(self,request):
		self.context['categories'] = Category.objects.all()
		self.context['subcategories'] = SubCategory.objects.all()
		self.context['sliders'] = Slider.objects.all()
		self.context['ads'] = Ad.objects.all()
		self.context['brands'] = Brand.objects.all()
		self.context['hots'] = Product.objects.filter(labels = 'hot')
		self.context['news'] = Product.objects.filter(labels = 'new')
		self.context['sales'] = Product.objects.filter(labels = 'sale')
		return render(request,'index.html',self.context)