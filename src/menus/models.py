from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from restaurants.models import RestaurantLocation
# Create your models here.
class Item(models.Model):
	#associations
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	restaurant = models.ForeignKey(RestaurantLocation)
	name = models.CharField(max_length=120)
	contents = models.TextField(help_text="Seperate each item by comma.")
	excludes = models.TextField(blank=True,null=True,help_text="Seperate each item by comma.")
	public = models.BooleanField(default=True)
	timestamp =models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def get_absolute_url(self):
		return reverse('menus:update',kwargs={'pk':self.pk})
	class Meta:
		ordering = ['-updated','-timestamp']

	def get_contents(self):
		return self.contents.split(",")
	def get_excludes(self):
		return self.excludes.split(",")
	def __str__(self):
		return self.name