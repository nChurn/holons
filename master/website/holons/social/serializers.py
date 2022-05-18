from rest_framework.serializers import ModelSerializer, CharField

from accounts.models import User


class UserSerializer(ModelSerializer):
    user_id = CharField(source='id')
    user_phone = CharField(source='phone_number')
    class Meta:
        model = User
        fields = ['user_id', 'username', 'user_phone', 'handle', 'userpic']