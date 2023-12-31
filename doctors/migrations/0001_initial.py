# Generated by Django 4.2.7 on 2023-11-08 15:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "doctorId",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("hospital", models.CharField(max_length=50)),
                ("doctorName", models.CharField(max_length=17)),
                ("department", models.TextField()),
                ("department_selfPay", models.TextField()),
                ("time_business", models.TextField()),
                ("time_lunch", models.TextField()),
            ],
        ),
    ]
