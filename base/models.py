import datetime
from django.db import models
from django.contrib.auth.models import *

# Create your models here.

class Users(AbstractUser):
    email = models.EmailField(null=True, unique=True, db_column='email')
    username =models.CharField(null =False,unique=True, max_length=50)
    telephone = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "Users"

class Post(models.Model):
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    image = models.FileField()
    type = models.IntegerField()
    date = models.DateTimeField()
    

    class Meta:
        db_table = "Post"

class Reaction(models.Model):
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

class Comment(models.Model):
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

class Reservation(models.Model):
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

class Internship(Post):
    typeStg = models.IntegerField()
    company = models.CharField(max_length=255)
    duration = models.IntegerField()
    subject = models.CharField(max_length=255)
    contactinfo = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)

    class Meta:
        db_table = "Internship"

    @property
    def cname(self):
       return "Stage"

class Accommodation(Post):
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contactinfo = models.CharField(max_length=255)

    class Meta:
        db_table = "Accommodation"

    @property
    def cname(self):
       return "Logement"

class Transport(Post):
    departure = models.CharField(max_length=255)
    departure_hour = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    seats = models.IntegerField()
    contactinfo = models.CharField(max_length=255)

    class Meta:
        db_table = "Transport"

    @property
    def cname(self):
       return "Transport"

class Recommendation(Post):
    text = models.CharField(max_length=255)
    
    class Meta:
        db_table = "Recommendation"

class Event(Post):
    titled = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    place = models.CharField(blank=True,max_length=255)
    contactinfo = models.CharField(blank=True,max_length=255)

    class Meta:
        abstract = True

class ClubEvent(Event):
    club = models.CharField(max_length=255)

    class Meta:
        db_table = "ClubEvent"

    @property
    def cname(self):
       return "Évènements scientifiques"

class SocialEvent(Event):
    price = models.FloatField(blank=True)

    class Meta:
        db_table = "SocialEvent"

    @property
    def cname(self):
       return "Évènements culturels"
    
class Notifications(models.Model):
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = "Notifications"