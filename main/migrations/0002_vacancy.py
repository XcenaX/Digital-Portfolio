# Generated by Django 3.0.5 on 2020-05-01 19:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('content', models.TextField(default='')),
                ('salary', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Employer')),
            ],
        ),
    ]
