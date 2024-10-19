from django.urls import path
from . import views

urlpatterns = [
    path('speed-test/', views.speed_test, name='speed_test'),
]
