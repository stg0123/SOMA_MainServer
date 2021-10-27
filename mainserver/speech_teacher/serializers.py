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

class PresentationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationFile
        fields = ('presentationfile_id','presentation_id','user_id','file_name','file')

class PresentationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationResult
        fields = ('presentation_result_id','presentation_id','user_id','presentation_result_audiofile','presentation_result_time','presentation_result_score',
        'presentation_result_dupword','presentation_result_improper','presentation_result_fillerwords','presentation_result_stammering',
        'presentation_result_gap','presentation_result_shake','presentation_result_tune','presentation_result_speed','presentation_result_date')