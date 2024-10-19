from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('speedload_app.urls')),  # اپلیکیشن شما
]
