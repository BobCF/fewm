from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField, IntegerField, DateTimeField

class User(AbstractUser):
    role=models.CharField(max_length=128)
    group=models.CharField(max_length=200)
    
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'tb_users'
        verbose_name = 'user'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    assignee =	models.CharField(max_length=255)
    tc_count =	models.IntegerField()
    tr_count =	models.IntegerField()
    bug_count =	models.IntegerField()
    testcycle_count =	models.IntegerField()
    total_exe_time =	models.IntegerField()
    avg_exe_time =	models.IntegerField()
    max_exe_time =	models.IntegerField()
    min_exe_time =	models.IntegerField()

class TaskCache(models.Model):
    tc_id =	models.IntegerField()
    configuration_id =	models.CharField(max_length=255)
    testcycle =	models.CharField(max_length=512)
    tcd_id =	models.IntegerField()
    tr_id =	models.IntegerField()
    priority =	models.CharField(max_length=255)
    status =	models.CharField(max_length=255)
    reason =	models.CharField(max_length=255)
    start_date =	models.DateTimeField()
    updated_date =	models.DateTimeField()
    assignee =	models.CharField(max_length=255)
    bug_id =	models.IntegerField()
    _updated_at =	models.DateTimeField()

class Task(models.Model):
    tc_id =	models.IntegerField()
    configuration_id =	models.CharField(max_length=255)
    testcycle =	models.CharField(max_length=512)
    tcd_id =	models.IntegerField()
    tr_id =	models.IntegerField()
    priority =	models.CharField(max_length=255)
    status =	models.CharField(max_length=255)
    reason =	models.CharField(max_length=255)
    start_date =	models.DateTimeField()
    updated_date =	models.DateTimeField()
    assignee =	models.CharField(max_length=255)
    bug_id =	models.IntegerField()
    _updated_at =	models.DateTimeField()
