from django.contrib import admin
from django.urls import path
from speedload_app import views  # ویوهای مربوط به speedload
from speedload_app import views as analyzer_views  # ویوهای مربوط به آنالیز سئو
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # صفحه اصلی
    path('admin/', admin.site.urls),  # پنل مدیریت
    path('speed-test/', views.speed_test, name='speed_test'),  # تست سرعت
    path('analyze/', analyzer_views.analyze_seo, name='analyze_seo'),  # آنالیز سئو
]

# اضافه کردن مسیر برای فایل‌های مدیا
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
