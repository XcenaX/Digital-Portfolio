# Generated by Django 3.0.5 on 2020-05-02 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_vacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
