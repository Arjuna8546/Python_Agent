from django.urls import path
from .views import *

urlpatterns = [
    path('add/',AddAgentDetails.as_view()),
    path('home/',Home.as_view())
]
