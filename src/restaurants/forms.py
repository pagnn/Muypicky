from django import forms
from restaurants.models import RestaurantLocation
from restaurants.validators import validate_category

class RestaurantCreateForm(forms.Form):
	name = forms.CharField()
	location = forms.CharField(required=False)
	category = forms.CharField(required=False)

	def clean_name(self):
		name=self.cleaned_data.get('name')
		if name == 'hello':
			raise forms.ValidationError('Not a valid name')
		return name

class RestaurantLocationCreateForm(forms.ModelForm):
	category=forms.CharField(required=False,validators=[validate_category])
	# email = forms.EmailField()
	class Meta:
		model=RestaurantLocation
		fields=[
			'name',
			'location',
			'category',
			'slug'
		]
	def clean_name(self):
		name=self.cleaned_data.get('name')
		if name == 'hello':
			raise forms.ValidationError('Not a valid name')
		return name
	# def clean_email(self):
	# 	email=self.cleaned_data.get('email')
	# 	if 'edu' in email:
	# 		raise forms.ValidationError('We do not accept edu emails.')
	# 	return email