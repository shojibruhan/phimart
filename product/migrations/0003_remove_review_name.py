# Generated by Django 4.2.20 on 2025-03-14 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_review"),
    ]

    operations = [
        migrations.RemoveField(model_name="review", name="name",),
    ]
