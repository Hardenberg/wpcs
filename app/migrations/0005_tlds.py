# Generated by Django 5.1.7 on 2025-03-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_wordpress_user_enumeration"),
    ]

    operations = [
        migrations.CreateModel(
            name="TLDS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tld", models.CharField(max_length=20)),
            ],
        ),
    ]
