from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField


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

class Task(models.Model):
    group_id = models.CharField(max_length=128, unique=True)
    title = models.TextField()

class UserProfile(models.Model):
    group_id = models.CharField(max_length=128, unique=True)
    title = models.TextField()