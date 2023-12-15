from rest_framework import serializers

class TestCycleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    eta_request_ww = serializers.CharField()
    case_complete = serializers.IntegerField()
    case_wip = serializers.IntegerField()
    case_notrun = serializers.IntegerField()
    case_blocked = serializers.IntegerField()
    release = serializers.CharField()
    plc_milestone = serializers.CharField()
    milestone_breakdown = serializers.CharField()
    owner = serializers.CharField()
    owner_team = serializers.CharField()
    start_date = serializers.DateTimeField()
    instance_id = serializers.CharField()

class TestStepSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    expect_result = serializers.CharField()

class TestCaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    configuration = serializers.CharField()
    status = serializers.CharField()
    owner = serializers.CharField()
    owner_team = serializers.CharField()
    tcd_id = serializers.IntegerField()
    test_steps = TestStepSerializer(many=True)
    active_test_step = serializers.CharField()

class TestResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField()
    reason = serializers.CharField()
    tag = serializers.CharField()
    actual_start = serializers.DateTimeField()
    complete = serializers.IntegerField()
    pause_start = serializers.DateTimeField()
    start_date = serializers.DateTimeField()
    total_pause_time = serializers.IntegerField()
    submitter = serializers.CharField()
    submitted_date = serializers.DateTimeField()
    