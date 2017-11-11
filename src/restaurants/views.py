from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView

from .models import RestaurantLocation
from .forms import RestaurantCreateForm,RestaurantLocationCreateForm

class RestaurantListView(LoginRequiredMixin,ListView):
	model=RestaurantLocation
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)

class RestaurantDetailView(LoginRequiredMixin,DetailView):
	template_name='restaurants/restaurantlocation_detail.html'
	model=RestaurantLocation
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)

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

class RestaurantUpdateView(LoginRequiredMixin,UpdateView):
	form_class=RestaurantLocationCreateForm
	template_name='restaurants/restaurant_detailview.html'
	def get_context_data(self,*args,**kwargs):
		context=super(RestaurantUpdateView,self).get_context_data(*args,**kwargs)
		context['title']='Add Restaurant'
		return context
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)