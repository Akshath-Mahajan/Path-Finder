from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('maps/', views.map, name='maps-map')
]
