# admin.py
from django.contrib import admin
from .models import Slider, Section
from .models import Sidebar



class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')  # نمایش عنوان و ترتیب در لیست مدیریت
    ordering = ('order',)  # ترتیب‌بندی براساس فیلد order

admin.site.register(Slider, SliderAdmin)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)

class SidebarAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')  # نمایش عنوان و آیکون در لیست
    search_fields = ('title',)  # قابلیت جستجو بر اساس عنوان

admin.site.register(Sidebar, SidebarAdmin)