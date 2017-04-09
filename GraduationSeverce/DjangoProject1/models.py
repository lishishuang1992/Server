from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Colordic(models.Model):
    ColorName = models.CharField(max_length=20)

class Personpaiming(models.Model):
    Name = models.CharField(max_length=20)
    Gender = models.CharField(max_length=20)




class AuthorList(models.Model):
    Name = models.CharField(max_length=10)

class AuthorList2(models.Model):
    Name = models.CharField(max_length=10)
class Book(models.Model):
    BookName = models.CharField(max_length=10,help_text='hhaha')
    Author = models.ManyToManyField(AuthorList)
