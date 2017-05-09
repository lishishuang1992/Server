from __future__ import unicode_literals

from django.db import models

# Create your models here.



class ball_user(models.Model):
    user_id = models.CharField(max_length=20)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    image = models.CharField(max_length=100,null=True)

class ball_table(models.Model):
    ball_ID = models.CharField(max_length=20)
    end_time = models.CharField(max_length=50)
    current_time = models.DateTimeField(auto_now_add=True)
    ball_object = models.CharField(max_length=50)
    money = models.CharField(max_length=20)
    project = models.CharField(max_length=10)
    ball_format = models.CharField(max_length=10)
    num_people = models.IntegerField(default=0)
    current_people = models.IntegerField(default=0)
    introduction = models.CharField(max_length=200)
    place = models.CharField(max_length=20)


class ball_enroll(models.Model):
    ball_id = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    status = models.CharField(max_length=10)


class about_ball(models.Model):
    user_id = models.CharField(max_length=20)
    ballMessage_id = models.CharField(max_length=20,null=True)
    ball_id = models.CharField(max_length=20,null=True)


class ball_message(models.Model):
    message_id = models.CharField(max_length=20)
    image = models.CharField(max_length=50)
    num = models.IntegerField(default=0)
    message = models.CharField(max_length=100)
    current_time = models.DateTimeField(auto_now_add=True)

class zan_message(models.Model):
    message_id = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)



