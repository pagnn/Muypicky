from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import View,DetailView,CreateView
# Create your views here.
from restaurants.models import RestaurantLocation
from menus.models import Item
from .models import Profile
from .forms import RegisterForm

User=get_user_model()
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile_ = qs.first()
            if not profile_.activated:
                user_ = profile_.user
                user_.is_active = True
                user_.save()
                profile_.activated = True
                profile_.activation_key=None
                profile_.save()
                return redirect("/login")
    return redirect("/login")
# class RegisterView(SuccessMessageMixin,CreateView):
# 	template_name='registration/register.html'
# 	form_class=RegisterForm
# 	success_url='/login/'
# 	success_message='Successly registered.'
# 	def dispatch(self,*args,**kwargs):
# 		if self.request.user.is_authenticated():
# 			return redirect('/login')
# 		return super(RegisterView,self).dispatch(*args,**kwargs)
def register(request):
	if request.method == 'POST':
		user_form = RegisterForm
		if user_form.is_valid():
			new_user=user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			return HttpResponse('Successfully')
		else:
			return HttpResponse('Sorry,you can not register.')
	else:
		user_form = RegisterForm()
		return render(request,'registration/register.html',{'form':user_form})
class ProfileFollowToggle(LoginRequiredMixin,View):
	def post(self,request,*args,**kwargs):
		username_to_toggle=request.POST.get('username')
		profile_,is_following=Profile.objects.toggle_follow(self.request.user,username_to_toggle)
		return redirect(f'/u/{profile_.user.username}/')
class RandomProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        return User.objects.filter(is_active=True, item__isnull=False).order_by("?").first() #/ gives a random item.

    def get_context_data(self, *args, **kwargs):
        context = super(RandomProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_following = False
        if self.request.user.is_authenticated():
            if user.profile in self.request.user.is_following.all():
                is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        items_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query)
        if items_exists and qs.exists():
            context['location'] = qs
        return context

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
