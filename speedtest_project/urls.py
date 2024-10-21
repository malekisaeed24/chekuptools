from django.contrib import admin
from django.urls import path
from speedload_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # صفحه اصلی
    path('admin/', admin.site.urls),  # پنل مدیریت
    path('speed-test/', views.speed_test, name='speed_test'),
]

# اضافه کردن مسیر برای فایل‌های مدیا
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
