# Generated by Django 4.2.20 on 2025-03-16 09:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_orderitem_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
