from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    userId = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    verificationCode = models.BigIntegerField(null=True)
    location = models.CharField(max_length=200,null=True)
    fieldOfInterest = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

class Parent(models.Model):
    name = models.CharField(max_length=200)
    userId = models.CharField(max_length=100)
    user = models.ForeignKey(User,models.DO_NOTHING)
    password = models.CharField(max_length=100)
    contact = models.BigIntegerField(null=True)

class Messages(models.Model):
    message = models.CharField(max_length=500)
    time = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    user = models.ForeignKey(User,models.DO_NOTHING)

class UserParent(models.Model):
    guardian = models.ForeignKey(Parent,models.DO_NOTHING)
    user = models.ForeignKey(User,models.DO_NOTHING)

