from django.urls import path,include
from .views import *

urlpatterns = [
    path('',HelloWorld),
    path('lookup/',lookup),
    path('user/',UserAPI.as_view()),
    path('login/',LoginAPI),
    path('changepw/',changepw),
    path('presentation/',UserPresentationAPI.as_view()),
    path('presentation/<int:pk>',PresentationAPI.as_view()),
]