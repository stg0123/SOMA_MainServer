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
    class Meta:
        managed = False # 자동 migration 하지않음
        db_table = "st_user" # 테이블 연결