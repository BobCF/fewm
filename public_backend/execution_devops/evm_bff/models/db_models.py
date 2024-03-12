from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField, IntegerField, DateTimeField, BigIntegerField, DurationField

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
    assignee =	models.CharField(max_length=255, null=True)
    tc_count =	models.IntegerField(null=True)
    tr_count =	models.IntegerField(null=True)
    bug_count =	models.IntegerField(null=True)
    testcycle_count =	models.IntegerField(null=True)
    total_exe_time =	models.IntegerField(null=True)
    avg_exe_time =	models.IntegerField(null=True)
    max_exe_time =	models.IntegerField(null=True)
    min_exe_time =	models.IntegerField(null=True)

class TaskCache(models.Model):
    tc_id =	models.BigIntegerField(null=True)
    configuration_id =	models.CharField(max_length=255, null=True)
    testcycle =	models.CharField(max_length=512, null=True)
    tcd_id =	models.BigIntegerField(null=True)
    tr_id =	models.BigIntegerField(null=True)
    priority =	models.CharField(max_length=255, null=True)
    status =	models.CharField(max_length=255, null=True)
    reason =	models.CharField(max_length=255, null=True)
    start_date =	models.DateTimeField(null=True)
    end_date =	models.DateTimeField(null=True)
    pause_date =	models.DateTimeField(null=True)
    pause_duration =	models.IntegerField(null=True)
    assignee =	models.CharField(max_length=255, null=True)
    bug_id =	models.BigIntegerField(null=True)
    _updated_at =	models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255, null=True)
    report_bug = models.CharField(max_length=255, null=True)
    test_env = models.CharField(max_length=255, null=True)

class Task(models.Model):
    tc_id =	models.BigIntegerField(null=True)
    configuration_id =	models.CharField(max_length=255, null=True)
    testcycle =	models.CharField(max_length=512, null=True)
    tcd_id =	models.BigIntegerField(null=True)
    tr_id =	models.BigIntegerField(null=True)
    priority =	models.CharField(max_length=255, null=True)
    status =	models.CharField(max_length=255, null=True)
    reason =	models.CharField(max_length=255, null=True)
    start_date =	models.DateTimeField(null=True)
    end_date =	models.DateTimeField(null=True)
    pause_date =	models.DateTimeField(null=True)
    pause_duration =	models.IntegerField(null=True)
    assignee =	models.CharField(max_length=255, null=True)
    bug_id =	models.BigIntegerField(null=True)
    _updated_at =	models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255, null=True)
    report_bug = models.CharField(max_length=255, null=True)
    test_env = models.CharField(max_length=255, null=True)
