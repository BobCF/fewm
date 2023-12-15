
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from evm_bff.models import TaskGroup, Task, TaskDsc, Flow


class FlowSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    dsc_id = serializers.IntegerField()
    task_id = serializers.IntegerField()
    step_id = serializers.IntegerField()
    result = serializers.CharField(required=False)
    assignee=serializers.CharField()
    start_time=serializers.DateTimeField(required=False)
    end_time=serializers.DateTimeField(required=False)
    pause_time=serializers.DateTimeField(required=False)
    create_at=serializers.DateTimeField(required=False)
    task_inst_id=serializers.CharField(required=False)
    comments=serializers.CharField(required=False)
    def create(self, validated_data):
        name = Flow.objects.create(**validated_data)
        return name
class TaskGroupSerializer(serializers.Serializer):
    # id=serializers.IntegerField(primary_key=True,auto_created=True)
    group_id = serializers.CharField()
    title = serializers.CharField()
    eta = serializers.CharField()
    team = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    size = serializers.IntegerField()
    status = serializers.CharField()
    configuration = serializers.CharField()
    group_inst_id = serializers.CharField()
    assignee=serializers.CharField()

    class Meta:
        managed=True

class TaskGroupSerializerupload(serializers.Serializer):
    # id=serializers.IntegerField(read_only=True)
    group_id = serializers.CharField(required=True,
                                     validators=[UniqueValidator(queryset=TaskGroup.objects.all(), message="group_id已经存在")])
    title = serializers.CharField()
    eta = serializers.CharField()
    team = serializers.CharField()
    # start_time = serializers.DateTimeField()
    # end_time = serializers.DateTimeField()
    size = serializers.IntegerField()
    status = serializers.CharField()
    configuration = serializers.CharField()
    # group_inst_id = serializers.CharField(max_length=40)
    assignee=serializers.CharField()

    def create(self, validated_data):
        name = TaskGroup.objects.create(**validated_data)
        return name
    # class Meta:
    #     validators = [
    #         UniqueTogetherValidator(
    #             queryset=TaskGroup.objects.all(),
    #             fields=("group_id")
    #         )
    #     ]
class TaskSerializer(serializers.Serializer):
    # id=serializers.IntegerField(read_only=True,required=False)
    task_id = serializers.CharField(required=True,
                                     validators=[UniqueValidator(queryset=Task.objects.all(), message="task_id已经存在")])
    task_title = serializers.CharField()
    group_id = serializers.CharField()
    dsc_id = serializers.CharField()
    task_inst_id = serializers.CharField(required=False)
    owner = serializers.CharField(required=False)
    stage = serializers.CharField(required=False)
    task_dsc = serializers.CharField(required=False)
    # task_action = serializers.CharField()
    # task_expection = serializers.CharField()
    # task_notes = serializers.CharField()
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    status = serializers.CharField()
    result = serializers.CharField(required=False)
    description=serializers.CharField()
    pre_condition=serializers.CharField()
    configuration=serializers.CharField()
    comments=serializers.CharField(required=False)
    def create(self, validated_data):
        name = Task.objects.create(**validated_data)
        return name
class TaskDscSerializer(serializers.Serializer):
    # id=serializers.IntegerField(primary_key=True,auto_created=True)
    dsc_id=serializers.CharField()
    task_id=serializers.CharField()
    status=serializers.CharField(required=False)
    step_id=serializers.IntegerField()
    title = serializers.CharField()
    configuration = serializers.CharField(required=False)
    action = serializers.CharField()
    expection = serializers.CharField()
    notes = serializers.CharField(required=False,allow_blank=True)
    def create(self, validated_data):
        name = TaskDsc.objects.create(**validated_data)
        return name
class AttachementSerializer(serializers.Serializer):
    # id = serializers.IntegerField(primary_key=True)
    group_id = serializers.IntegerField()
    task_desc_id = serializers.IntegerField()
    task_id = serializers.IntegerField()
    url = serializers.CharField()
    file_type = serializers.CharField()

class ConfigurationSerializer(serializers.Serializer):
    # id = serializers.IntegerField(primary_key=True)
    title = serializers.CharField()
    key = serializers.CharField()
    value = serializers.CharField()

class UsersrigraSerializer(serializers.Serializer):
    role=serializers.CharField()
    group=serializers.CharField()
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.username
class newSerializer(serializers.Serializer):
    # id=serializers.IntegerField(primary_key=True)
    username=serializers.CharField()
    password=serializers.CharField()
    role=serializers.CharField()
    date_joined=serializers.DateTimeField()
    group=serializers.CharField()
