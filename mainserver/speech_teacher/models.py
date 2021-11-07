from django.db import models
import boto3
from django.core.cache import cache

class ST_User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=255, null=False)
    user_password = models.TextField(null = False)
    user_nickname = models.CharField(max_length=255)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        cache.delete('users')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('users')
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.user_email)

    class Meta:
        managed = False # 자동 migration 하지않음
        db_table = "st_user" # 테이블 연결

class Presentation(models.Model):
    presentation_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("ST_User",related_name='user_presentation',on_delete=models.CASCADE,db_column='user_id')
    presentation_title = models.CharField(max_length=20,null=False)
    presentation_time = models.TimeField(null=False)
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

class PresentationFile(models.Model):
    presentationfile_id = models.AutoField(primary_key=True)
    presentation_id = models.ForeignKey("presentation",related_name='presentation_file',on_delete=models.CASCADE,db_column='presentation_id',null=False)
    user_id = models.IntegerField(null=False)
    file_name = models.TextField(null=False)
    file = models.FileField(upload_to='presentation_file')

    def __str__(self):
        return str(self.file_name)
    
    # def delete(self, *args, **kwargs):
    #     super().delete(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'presentation_file'

class PresentationResult(models.Model):
    presentation_result_id = models.AutoField(primary_key=True)
    presentation_id = models.ForeignKey("presentation",related_name='presentation_result',on_delete=models.CASCADE,db_column='presentation_id',null=False)
    user_id = models.IntegerField(null=False)
    presentation_result_audiofile = models.FileField(upload_to='audio_file')
    presentation_result_time = models.IntegerField(null = False)
    presentation_result = models.JSONField(null=False)
    presentation_result_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.presentation_result_date)+' '+str(self.presentation_id)+' presentation result'
    
    class Meta:
        managed = False
        db_table = 'presentation_result'

class Knowhow(models.Model):
    knowhow_id = models.AutoField(primary_key=True)
    knowhow_title = models.CharField(max_length=255)
    knowhow_img = models.FileField(upload_to='knowhow_img',null=True,blank=True)
    knowhow_contents = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return str(self.knowhow_title)

    class Meta:
        managed = False
        db_table = 'knowhow'
     
