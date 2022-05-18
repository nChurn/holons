from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer

from moneta.models import FixedCost, CostTag, VariableCost
from purpose.serializers import ContextSerializer

class CostTagSerializer(ModelSerializer):
    owner_id = CharField()
    context_id = IntegerField(required=True)
    class Meta:
        model = CostTag
        fields = ['id', 'owner_id', 'name', 'uses_count', 'context_id']
        read_only_fields = ['uses_count']

class FixedCostSerializer(ModelSerializer):
    owner_id = CharField()
    tags = CostTagSerializer(many=True, read_only=True)
    context_id = IntegerField(required=True)
    # context = ContextSerializer(read_only=True)
    class Meta:
        model = FixedCost
        fields = ['id', 'owner_id', 'context_id', 'amount', 'name', 'started_at', 'finished_at', 'tags']

class VariableCostSerializer(ModelSerializer):
    owner_id = CharField()
    tags = CostTagSerializer(many=True, read_only=True)
    context_id = IntegerField(required=True)
    class Meta:
        model = VariableCost
        fields = ['id', 'owner_id', 'context_id', 'amount', 'name', 'date', 'tags']