from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_email','user_password','user_nickname','user_create_date','user_update_date')

class ST_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ST_User
        fields = ('user_id','user_email','user_password','user_nickname','user_create_date','user_update_date')