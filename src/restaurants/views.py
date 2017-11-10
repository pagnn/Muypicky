from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,CreateView

from .models import RestaurantLocation
from .forms import RestaurantCreateForm,RestaurantLocationCreateForm

@login_required()
def restaurant_createview(request):
	form=RestaurantLocationCreateForm(request.POST or None)
	errors=None
	if form.is_valid():
		if request.user.is_authenticated():
			instance=form.save(commit=False)
			instance.owner=request.user
			instance.save()
			return HttpResponseRedirect('/restaurants/')
		else:
			return HttpResponseRedirect('/login/')
	if form.errors:
		errors = form.errors
	template_name='restaurants/form.html'
	context={
		'form':form,
		'errors':errors
	}
	return render(request,template_name,context)
def restaurants_listview(request):
	template_name='restaurants/restaurantlocation_list.html'
	queryset=RestaurantLocation.objects.all()
	context={
		'queryset':queryset
	}
	return render(request,template_name,context)
def restaurant_detailview(request,slug):
	template_name='restaurants/restaurantlocation_detail.html'
	obj=RestaurantLocation.objects.get(slug=slug)
	context={
		"object":obj
	}
	return render(request,template_name,context)

class RestaurantListView(ListView):
	model=RestaurantLocation
	def get_queryset(self):
		slug=self.kwargs.get("slug")
		if slug:
			queryset=RestaurantLocation.objects.filter(
				Q(category__iexact=slug) |
				Q(category__icontains=slug)
				)
		else:
			queryset=RestaurantLocation.objects.all()
		return queryset

class RestaurantDetailView(DetailView):
	template_name='restaurants/restaurantlocation_detail.html'
	model=RestaurantLocation
	queryset=RestaurantLocation.objects.all()
	# def get_object(self,*args,**kwargs):
	# 	rest_id=self.kwargs.get('rest_id')
	# 	obj=get_object_or_404(RestaurantLocation,id=rest_id)
	# 	return obj

	# def get_context_data(self,*args,**kwargs):
	# 	context=super(RestaurantDetailView,self).get_context_data(*args,**kwargs)
	# 	return context


class RestaurantCreateView(LoginRequiredMixin,CreateView):
	form_class=RestaurantLocationCreateForm
	template_name='form.html'
	def get_context_data(self,*args,**kwargs):
		context=super(RestaurantCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Add Restaurant'
		return context


	def form_valid(self,form):
		instance=form.save(commit=False)
		instance.owner=self.request.user
		return super(RestaurantCreateView,self).form_valid(form)
