# Generated by Django 5.1.2 on 2024-10-21 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speedload_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='slider',
            name='link',
            field=models.URLField(default='http://example.com'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='slider',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
