from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField


class Flow(models.Model):
    group_id = models.CharField(max_length=64)
    dsc_id = models.CharField(max_length=64)
    task_id = models.CharField(max_length=64)
    step_id = models.CharField(max_length=64)
    result = models.CharField(max_length=64)
    assignee=models.CharField(max_length=128, null=True)
    start_time=models.DateTimeField(default=None, null=True)
    works_time=models.IntegerField()
    end_time=models.DateTimeField(default=None, null = True)
    pause_time=models.DateTimeField(default=None, null = True)
    create_at=models.DateTimeField(auto_now_add=True)
    task_inst_id=models.CharField(max_length=128)
    comments=models.CharField(max_length=128)
    execution_id=models.CharField(max_length=128, null=True)
	
    def to_json(self):
        return {
            'test_cycle_id': self.group_id,
            'test_case_id': self.task_id,
            'asignee': self.assignee,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'pause_time': self.pause_time,
            'create_at': self.create_at,
            'test_case_result': self.test_case_result,
        }

	
class TaskGroup(models.Model):
    # id=models.IntegerField(primary_key=True,auto_created=True)
    group_id = models.CharField(max_length=128, unique=True)
    title = models.TextField()
    eta = models.CharField(max_length=64)
    team = models.CharField(max_length=64)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    size = models.IntegerField()
    status = models.CharField(max_length=32)
    configuration = models.CharField(max_length=200)
    group_inst_id = models.CharField(max_length=40)
    assignee=models.CharField(max_length=128)

    class Meta:
        managed=True


class Task(models.Model):
    # id=models.IntegerField(primary_key=True,AUTO_INCREMENT=True)
    task_id = models.CharField(max_length=100)
    task_title = models.TextField()
    group_id = models.CharField(max_length=100)
    dsc_id = models.CharField(max_length=128)
    task_inst_id = models.CharField(max_length=40)
    owner = models.CharField(max_length=64)
    stage = models.CharField(max_length=64)
    task_dsc = models.TextField()
    # task_action = models.TextField()
    # task_expection = models.TextField()
    # task_notes = models.TextField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=32)
    result = models.CharField(max_length=64)
    description=models.TextField()
    pre_condition=models.TextField()
    configuration=models.TextField()
    comments=models.TextField()
    running=BooleanField(default=False)

class TaskDsc(models.Model):
    # id=models.IntegerField(primary_key=True,auto_created=True)
    dsc_id=models.CharField(max_length=128)
    task_id=models.CharField(max_length=64)
    status=models.CharField(max_length=128)
    step_id=models.BigIntegerField()
    title = models.TextField()
    configuration = models.CharField(max_length=32)
    action = models.TextField()
    expection = models.TextField()
    notes = models.TextField()

class Attachement(models.Model):
    id = models.BigIntegerField(primary_key=True)
    group_id = models.IntegerField()
    task_desc_id = models.IntegerField()
    task_id = models.IntegerField()
    url = models.TextField()
    file_type = models.CharField(max_length=16)

class Configuration(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=128)

class Usersrigra(AbstractUser):
    role=models.CharField(max_length=128)
    group=models.CharField(max_length=200)
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.username
class new(models.Model):
    id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=128)
    role=models.CharField(max_length=128)
    date_joined=models.DateTimeField(auto_now_add=True)
    group=models.CharField(max_length=64)
