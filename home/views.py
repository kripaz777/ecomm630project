from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class Base(View):
	context = {}

class HomeView(Base):
	def get(self,request):

		return render(request,'index.html')