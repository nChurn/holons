from rest_framework.serializers import ModelSerializer, CharField, IntegerField

from .models import CheckIn, Context, KeyResult, KeyResultType, Objective, Purpose
from social.serializers import UserSerializer

class ContextSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True) 
    class Meta: 
        model = Context
        fields = ['id', 'type', 'foreign', 'owner']

class CheckInSerializer(ModelSerializer):
    class Meta:
        model = CheckIn
        exclude = ['key_result']

class ShortPurposeSerializer(ModelSerializer):
    class Meta:
        model = Purpose
        fields = ['id', 'title', 'status', 'start_at']

class KeyResultSerializer(ModelSerializer):
    objective_id = IntegerField()
    type_id = IntegerField(write_only=True)
    owner_id = CharField(write_only=True, allow_null=True, required=False)

    owner = UserSerializer(read_only=True) 
    creator = UserSerializer(read_only=True)
    context = ContextSerializer(read_only=True)
    purpose = ShortPurposeSerializer(read_only=True)
    next_check_in = CheckInSerializer(read_only=True)

    check_ins = CheckInSerializer(many=True, read_only=True)
    class Meta:
        model = KeyResult
        fields = [
            'id', 'title', 'done_at', 'current_value', 'target_value', 'type', 
            'type_id', 'objective_id', 'owner_id', 'owner', 'creator', 'interval', 
            'context', 'purpose', 'check_ins', 'next_check_in'
        ]
        read_only_fields = ['type', 'done_at', 'owner']
        depth = 2

class ObjectiveSerializer(ModelSerializer):
    purpose_id = IntegerField()
    key_results = KeyResultSerializer(many=True, read_only=True)
    class Meta:
        model = Objective
        fields = ['id', 'title', 'purpose_id', 'key_results', 'is_done']
        read_only_fields = ['is_done']
        depth = 2

class PurposeSerializer(ModelSerializer):
    owner_id = CharField()
    context = ContextSerializer(read_only=True)
    context_id = IntegerField(write_only=True)
    objectives = ObjectiveSerializer(many=True, read_only=True)
    class Meta:
        model = Purpose
        fields = ['id', 'title', 'context', 'owner_id', 'objectives', 'status', 'start_at', 'context_id', 'finish_at', 'plan_end_date']
        read_only_fields = ['finish_at']
        extra_kwargs = {'context_id': {'write_only': True}}
        depth = 1

class KeyResultTypeSerializer(ModelSerializer):
    class Meta:
        model = KeyResultType
        fields = ['id', 'name']