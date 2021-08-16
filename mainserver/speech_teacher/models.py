from django.db import models
from django.db.models import manager

class ST_User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    user_nickname = models.CharField(max_length=255)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_email)

    class Meta:
        managed = False # 자동 migration 하지않음
        db_table = "st_user" # 테이블 연결

class Presentation(models.Model):
    presentation_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("ST_User",related_name='user_presentation',on_delete=models.CASCADE,db_column='user_id')
    presentation_title = models.CharField(max_length=20)
    presentation_time = models.IntegerField(null= False)
    presentation_date = models.DateField(null=False)
    presentation_update_date = models.DateTimeField(auto_now=True)
    presentation_ex_dupword = models.TextField(null=True,blank=True)
    presentation_ex_improper = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.presentation_title)

    class Meta:
        managed = False
        db_table = "presentation"

class KeyWord(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    presentation_id = models.ForeignKey("Presentation",related_name='presentation_keyword',on_delete=models.CASCADE,db_column='presentation_id')
    keyword_page = models.IntegerField(null=False)
    keyword_contents = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.presentation_id)+' '+str(self.keyword_page)+'page keyword'

    class Meta:
        managed =False
        db_table = 'keyword'

class Script(models.Model):
    script_id = models.AutoField(primary_key=True)
    presentation_id = models.ForeignKey("Presentation",related_name='presentation_script',on_delete=models.CASCADE,db_column='presentation_id')
    script_page = models.IntegerField(null= False)
    script_contents = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.presentation_id)+' '+str(self.keyword_page)+'page script'
    
    class Meta:
        managed = False
        db_table = 'script'