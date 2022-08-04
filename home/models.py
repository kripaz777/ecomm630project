from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 300)
	slug = models.CharField(max_length = 300)
	icon = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length = 300)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	slug = models.CharField(max_length = 300)
	icon = models.CharField(max_length = 100)

	def __str__(self):
		return self.name