from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import View,DetailView,CreateView
# Create your views here.
from restaurants.models import RestaurantLocation
from menus.models import Item
from .models import Profile
from .forms import RegisterForm

User=get_user_model()
class RegisterView(CreateView):
	template_name='registration/register.html'
	form_class=RegisterForm
	success_url='/login'

class ProfileFollowToggle(LoginRequiredMixin,View):
	def post(self,request,*args,**kwargs):
		username_to_toggle=request.POST.get('username')
		profile_,is_following=Profile.objects.toggle_follow(self.request.user,username_to_toggle)
		return redirect(f'/u/{profile_.user.username}/')
class ProfileDetailView(DetailView):
	template_name='profiles/user.html'

	def get_object(self):
		username=self.kwargs.get("username")
		if username == None:
			raise Http404
		return get_object_or_404(User,username__iexact=username,is_active=True)

	def get_context_data(self,*args,**kwargs):
		context=super(ProfileDetailView,self).get_context_data(*args,**kwargs)
		user=context['user']
		item_exist=Item.objects.filter(user=self.get_object()).exists()
		is_following=False
		if user.profile in self.request.user.is_following.all():
			is_following=True
		context['is_following']=is_following
		query=self.request.GET.get("q")
		qs=RestaurantLocation.objects.filter(owner=self.get_object()).search(query)
		if item_exist and qs.exists():
			context['location']=qs
		return context
