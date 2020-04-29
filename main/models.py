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

class Request(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(Employer, on_delete=models.CASCADE, default=None)
    is_applied = models.BooleanField(default=False)
    def __str__(self):
        return self.content

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
    achivements = models.ManyToManyField(Achivement, null=True, blank=True)
    requests = models.ManyToManyField(Request, null=True, blank=True)
    views = models.ManyToManyField(View, blank=True)
    vk = models.TextField(default="")
    telegram = models.TextField(default="")
    about = models.TextField(default="") 
    def __str__(self):
        return self.username



