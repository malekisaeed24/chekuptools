from django.db import models



class Slider(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sliders/')
    link = models.URLField(default='http://example.com')  # مقدار پیش‌فرض برای فیلد link

    order = models.PositiveIntegerField(default=0)  # فیلد order برای ترتیب‌بندی

    def __str__(self):
        return self.title

class Section(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=200, blank=True)
    order = models.IntegerField(default=0)  # فیلد order برای ترتیب
    image = models.ImageField(upload_to='sections/', blank=True, null=True)  # فیلد تصویر کوچک

    def __str__(self):
        return self.title


from django.db import models

class Sidebar(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    icon = models.ImageField(upload_to='sidebar_icons/')  # فیلد برای آپلود تصویر

    def __str__(self):
        return self.title


