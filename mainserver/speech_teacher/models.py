from django.db import models

# Create your models here.
class User(models.Model):
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_nickname = models.CharField(max_length=50)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_update_date = models.DateTimeField(auto_now=True)