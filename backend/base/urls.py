from django.urls import path
from .views import *

urlpatterns = [
    path('add/',AddAgentDetails.as_view()),
    path('home/',Home.as_view()),
    path('subprocess/<int:pid>/', SubprocessView.as_view(), name='subprocess'),
    path('processes/<int:sid>/', ProcessView.as_view(), name='process'),
]
