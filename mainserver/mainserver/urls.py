from django.contrib import admin
from django.urls import path,include,re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view( 
    openapi.Info( 
        title="Swagger API 명세서", 
        default_version="v1", 
        description="말선생 프로젝트를 위한 api 명세서", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="이메일", email="sontg123@naver.com"), 
        license=openapi.License(name=""), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)



urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('',include('speech_teacher.urls')),
    path('admin/', admin.site.urls),
]
