from django.urls import path, re_path

from . import views


urlpatterns = [

	# re_path(r'travel/^(?P<source>[a-zA-Z0-9_-])$', views.index, name='index')]

	path("", views.index, name='index'),

]