# Generated by Django 5.1.1 on 2024-09-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_app', '0004_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pet',
            name='vaccination',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
