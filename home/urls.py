from .views import *
from django.urls import path

urlpatterns = [
		path('', HomeView.as_view(), name='home'),
		path('category/<slug>', CategoryView.as_view(), name='category'),
		path('detail/<slug>', DetailView.as_view(), name='detail'),
		path('search', SearchView.as_view(), name='search'),
		path('signup', signup, name='signup'),
		path('cart',CartView.as_view(),name='cart'),
		path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),
		path('delete-cart/<slug>',delete_product,name='delete-cart'),
		path('reduce-product/<slug>',reduce_product,name='reduce-product'),
		path('product_review/<slug>',product_review,name='product_review')
]