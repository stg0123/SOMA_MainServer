from django.urls import path,include
from .views import *

urlpatterns = [
    path('',HelloWorld),
    path('user/',UserAPI.as_view()),
    path('login/',LoginAPI),
    path('changepw/',changepw),
]