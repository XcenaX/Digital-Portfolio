from django.db import models
from django.utils import timezone
from django.conf import settings

class City(models.Model):
    name = models.TextField(default="")

class University(models.Model):
    name = models.TextField(default="")
    city = models.OneToOneField(City, on_delete=models.CASCADE, primary_key=True)

class Achivement(models.Model):
    description = models.TextField()
    img_url = models.TextField(default="")
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description

class Employer(models.Model): # работодатель
    email = models.TextField(default="") 
    password = models.TextField(default="") 
    username = models.TextField(default="") 
    fullname= models.TextField(default="") 
    img_url = models.TextField(default=settings.STATIC_URL+"images/icons/user.png")
    date_of_register = models.DateField(auto_now=True) 
    is_active = models.BooleanField(default=False)
    description = models.TextField(default="")
    vk = models.TextField(default="")
    telegram = models.TextField(default="")
    def __str__(self):
        return self.username

class View(models.Model):
    owner = models.ForeignKey(Employer, on_delete=models.CASCADE)

class Student(models.Model):
    is_searching_work = models.BooleanField(default=True)
    email = models.TextField(default="") 
    password = models.TextField(default="") 
    username = models.TextField(default="") 
    fullname= models.TextField(default="") 
    img_url = models.TextField(default=settings.STATIC_URL+"images/icons/user.png")
    medcard_url = models.TextField(default="", blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    university_course = models.IntegerField(null=True, blank=True)
    specialty = models.TextField(default="", blank=True)
    date_of_birth = models.DateField(null=True, blank=True) 
    date_of_register = models.DateField(auto_now=True) 
    is_active = models.BooleanField(default=False)
    achivements = models.ManyToManyField(Achivement, null=True, related_name='achivements',  blank=True)
    views = models.ManyToManyField(View, blank=True, related_name='views')
    vk = models.TextField(default="")
    telegram = models.TextField(default="")
    about = models.TextField(default="") 
    def __str__(self):
        return self.username


class Vacancy(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
    salary = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(Employer, on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=True)
    views = models.ManyToManyField(View, blank=True)
    def __str__(self):
        return self.title


class Request(models.Model):
    pub_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(Employer, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, default=None)
    is_applied = models.BooleanField(default=False)
    def __str__(self):
        return self.student.fullname


class Applied_Vacancy(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.vacancy.title