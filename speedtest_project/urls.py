from django.urls import path
from speedload_app import views

urlpatterns = [
    path('speed-test/', views.speed_test, name='speed_test'),
]
