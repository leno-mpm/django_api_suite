from django.urls import path
from .views import LandingAPI
from .views import LandingAPIItem


urlpatterns = [
    path('index/', LandingAPI.as_view(), name='landing-index'),
    path('index/<str:item_id>/', LandingAPIItem.as_view(), name='landing-item'),
]
