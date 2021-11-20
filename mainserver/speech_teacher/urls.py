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
    path('keyword/<int:presentation_id>',KeyWordAPI.as_view()),
    path('script/<int:presentation_id>',ScriptAPI.as_view()),
    path('allfile/',AllFileAPI.as_view()),
    path('presentationfile/<int:presentation_id>',PresentationFileAPI.as_view()),
    path('presentationresult/<int:presentation_id>',PresentationResultAPI.as_view()),
    path('presentationresultdetail/<int:presentation_result_id>',PresentationResultDetailAPI.as_view()),
    path('knowhow/',KnowhowAPI.as_view()),
    path('test/',TestAPI.as_view()),
    path('test/<int:testdb_id>',TESTgetAPI),
]



