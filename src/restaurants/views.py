from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from .models import RestaurantLocation

def restaurants_listview(request):
	template_name='restaurants/restaurantlocation_list.html'
	queryset=RestaurantLocation.objects.all()
	context={
		'queryset':queryset
	}
	return render(request,template_name,context)

class RestaurantListView(ListView):
	def get_queryset(self):
		slug=self.kwargs.get("slug")
		if slug:
			queryset=RestaurantLocation.objects.filter(
				Q(category__iexact=slug)|
				Q(category__icontains=slug)
				)
		else:
			queryset=RestaurantLocation.objects.all()
		return queryset
class RestaurantDetailView(DetailView):
	queryset=RestaurantLocation.objects.all()

