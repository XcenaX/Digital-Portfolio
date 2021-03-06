# Generated by Django 3.0.5 on 2020-05-04 00:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achivement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('img_url', models.TextField(default='')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(default='')),
                ('password', models.TextField(default='')),
                ('username', models.TextField(default='')),
                ('fullname', models.TextField(default='')),
                ('img_url', models.TextField(default='/static/images/icons/user.png')),
                ('date_of_register', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('description', models.TextField(default='')),
                ('vk', models.TextField(default='')),
                ('telegram', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('name', models.TextField(default='')),
                ('city', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.City')),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('content', models.TextField(default='')),
                ('salary', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Employer')),
                ('views', models.ManyToManyField(blank=True, to='main.View')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_searching_work', models.BooleanField(default=True)),
                ('email', models.TextField(default='')),
                ('password', models.TextField(default='')),
                ('username', models.TextField(default='')),
                ('fullname', models.TextField(default='')),
                ('img_url', models.TextField(default='/static/images/icons/user.png')),
                ('medcard_url', models.TextField(blank=True, default='')),
                ('university_course', models.IntegerField(blank=True, null=True)),
                ('specialty', models.TextField(blank=True, default='')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_register', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('vk', models.TextField(default='')),
                ('telegram', models.TextField(default='')),
                ('about', models.TextField(default='')),
                ('achivements', models.ManyToManyField(blank=True, null=True, to='main.Achivement')),
                ('views', models.ManyToManyField(blank=True, to='main.View')),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.University')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_applied', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Employer')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Student')),
                ('vacancy', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Vacancy')),
            ],
        ),
        migrations.CreateModel(
            name='Applied_Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Student')),
                ('vacancy', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Vacancy')),
            ],
        ),
    ]
