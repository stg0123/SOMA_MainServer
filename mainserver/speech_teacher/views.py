from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *
from .serializers import *


# Create your views here.
@api_view(['GET'])
def HelloWorld(request):
    return Response("hello world!")


class UserAPI(APIView):
    """
        유저 생성,조회 api
        
        ---
        ## 내용
        - 유저 생성 : post 방식으로 user_email,user_password,user_nickname속성 필수
        - 유저 조회 : get 방식으로 요청값 없음
    """
    def post(self,request):
        serializer = UserSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def get(self,request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset,many=True)
        return Response(serializer.data)


    


