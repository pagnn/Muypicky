import random
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#function based on view
def home(request):
	num=random.randint(1,1000000)
	context={
		"bool_item":True,
		"num":num
	}
	return render(request,'base.html',context)#response
