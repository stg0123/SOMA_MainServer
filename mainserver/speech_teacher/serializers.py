from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_email','user_password','user_nickname','user_create_date','user_update_date')


class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = ('presentation_id','user_id','presentation_title','presentation_time','presentation_date','presentation_update_date','presentation_ex_dupword','presentation_ex_improper')



class ST_UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ST_User
        fields = ('user_id','user_email','user_password','user_nickname','user_create_date','user_update_date')