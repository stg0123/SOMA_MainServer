from mainserver.settings import SECRET_KEY
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import *
from .serializers import *
from .utils import login_check
import bcrypt
import re
import jwt
# Create your views here.
@api_view(['GET'])
def HelloWorld(request):
    return Response("hello world!")

@api_view(['POST'])
def LoginAPI(request):
    data = request.data
    try:
        input_email =data["user_email"]
        input_password = data["user_password"].encode('utf-8')
    except Exception :
        return Response({'massage':'KEY_ERROR'},status=400)
    
    try:
        user_ck = ST_User.objects.get(user_email = input_email)
    except Exception:
        return Response({'message':'INVALID_USER'},status=400)

    if bcrypt.checkpw(input_password,user_ck.user_password.encode('utf-8')):
        access_token = jwt.encode({'user_id':user_ck.user_id},SECRET_KEY,algorithm='HS256')
        print(access_token)
        print(jwt.decode(access_token,SECRET_KEY,algorithms='HS256'))
        return Response({'message':'success', 'access_token':access_token},status=200)

    return Response({"massage" : "INVALID_PASSWORD"},status=400)



class UserAPI(APIView):
    """
        유저 생성,조회 api
        
        ---
        ## 내용
        - 유저 생성(회원가입) : post 방식으로 user_email,user_password,user_nickname속성 필수
        - 유저 조회 : get 방식으로 요청값 없음
    """
    def post(self,request):
        # print(request._request.headers)
        # print(request._request.headers['Authorization'])
        # print(request._request.body)  # body는 byte 타입이므로 딕셔너리 형태로 사용하기 위해서는 json.loads()를 이용하여 decoding 필요
        # print(request.data)
    
        # test1 = ST_User.objects.get(user_email = 'test1@test.com')  # get 의 경우 딱 1개가 아닐경우 예외가 발생\
        # print(test1)
        # print(test1.user_email)

        email_regex= '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        data = request.data
        serializer = ST_UserSerializer(data= request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)

        if not re.search(email_regex,data['user_email']):
            return Response({"message": "invalid email"}, status = 400)

        if ST_User.objects.filter(user_email =data['user_email']) :
            return Response({"message":"email is already exist"},status=400)

        if ST_User.objects.filter(user_nickname = data['user_nickname']):
            return Response({"message":"nickname is already exist"},status=400)
            
        hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        ST_User(user_email = data['user_email'],user_password = hashed_password,user_nickname = data['user_nickname']).save()
        # ST_User.objects.create(user_email = data['user_email'],user_password = hashed_password ,user_nickname = data['user_nickname'])
        return Response({"message" : "success"},status=200)
    
    @login_check
    def get(self,request):
        serializer = ST_UserSerializer(request.user)
        return Response(serializer.data)
    
    @login_check
    def put(self,request):
        serializer =ST_UserSerializer(request.user)
        print(serializer.data)
        data = request.data
        if serializer.data['user_email'] != data['user_email']:
            print(1)
            request.user.user_email = data['user_email']
        if not bcrypt.checkpw(data['user_password'].encode('utf-8'),serializer.data['user_password'].encode('utf-8')):
            print(2)
            hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            request.user.user_password= hashed_password
        if serializer.data['user_nickname'] != data['user_nickname']:
            print(3)
            request.user.user_nickname=data['user_nickname']
        request.user.save()
        
        return Response({'message':'success'},status=200)
    
    @login_check
    def delete(self,request):
        user_email = request.user.user_email
        request.user.delete()
        return Response({'message': user_email+" is delete success"},status=200)


