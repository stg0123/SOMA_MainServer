from django.db import models

# Create your models here.
class User(models.Model):
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_nickname = models.CharField(max_length=50)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_update_date = models.DateTimeField(auto_now=True)

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