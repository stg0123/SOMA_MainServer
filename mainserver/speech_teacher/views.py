from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *
from .serializers import *
import bcrypt
import re
# Create your views here.
@api_view(['GET'])
def HelloWorld(request):
    return Response("hello world!")


class UserAPI(APIView):
    """
        유저 생성,조회 api
        
        ---
        ## 내용
        - 유저 생성(회원가입) : post 방식으로 user_email,user_password,user_nickname속성 필수
        - 유저 조회 : get 방식으로 요청값 없음
    """
    def post(self,request):
        print(request._request.headers)
        print(request._request.body)
        print(request.data)
        email_regex= '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        data = request.data
        serializer = ST_UserSerializer(data= request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        if not re.search(email_regex,data['user_email']):
            return Response({"message": "invalid email"}, status = 400)
        #User.objects.get(user_email = 'test@test.com')  # get 의 경우 딱 1개가 아닐경우 예외가 발생
        if ST_User.objects.filter(user_email =data['user_email']) :
            return Response({"message":"email is already exist"},status=400)
        if ST_User.objects.filter(user_nickname = data['user_nickname']):
            return Response({"message":"nickname is already exist"},status=400)
        hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        ST_User.objects.create(user_email = data['user_email'],user_password = hashed_password ,user_nickname = data['user_nickname'])
        return Response({"message" : "success"},status=200)

    def get(self,request):
        queryset = ST_User.objects.all()
        serializer = ST_UserSerializer(queryset,many=True)
        print(serializer.data)
        return Response(serializer.data)


    


