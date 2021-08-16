from rest_framework import serializers
from .models import *

class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = ('presentation_id','user_id','presentation_title','presentation_time','presentation_date','presentation_update_date','presentation_ex_dupword','presentation_ex_improper')

class ST_UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ST_User
        fields = ('user_id','user_email','user_password','user_nickname','user_create_date','user_update_date')

class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = ('keyword_id','presentation_id','keyword_page','keyword_contents')

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('script_id','presentation_id','script_page','script_contents')