# admin.py
from django.contrib import admin
from .models import Slider, Section


class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')  # نمایش عنوان و ترتیب در لیست مدیریت
    ordering = ('order',)  # ترتیب‌بندی براساس فیلد order

admin.site.register(Slider, SliderAdmin)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)

