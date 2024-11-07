from django.contrib import admin
from .models import Slider, Section, Sidebar

def copy_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # ایجاد یک آیتم جدید با حذف شناسه اصلی (pk)
        obj.save()

copy_selected.short_description = "کپی موارد انتخاب شده"

class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)
    actions = [copy_selected]  # اضافه کردن اکشن به لیست اکشن‌ها

admin.site.register(Slider, SliderAdmin)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)
    actions = [copy_selected]  # اضافه کردن اکشن به لیست اکشن‌ها

class SidebarAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
    search_fields = ('title',)
    actions = [copy_selected]  # اضافه کردن اکشن به لیست اکشن‌ها

admin.site.register(Sidebar, SidebarAdmin)
