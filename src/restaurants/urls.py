from django.conf.urls import url

from .views import (
	RestaurantListView,
	RestaurantDetailView,
    RestaurantCreateView,
    RestaurantUpdateView
	)


urlpatterns = [
    # url(r'^restaurants/create/$',restaurant_createview),
    url(r'^create/$',RestaurantCreateView.as_view(),name='create'),
    url(r'^$',RestaurantListView.as_view(),name='list'),
    # url(r'^(?P<slug>[\w-]+)/$',RestaurantDetailView.as_view(),name='detail'),
    url(r'^(?P<slug>[\w-]+)/$',RestaurantUpdateView.as_view(),name='update')
]
