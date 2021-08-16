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

@api_view(['POST'])
def changepw(request):
    data = request.data
    try:
        input_email = data['user_email']
        input_password = data['user_password'].encode('utf-8')
    except Exception:
        return Response({'massage': 'KEY_ERROR'},status=400)
    user = ST_User.objects.get(user_email = input_email)
    user.user_password= bcrypt.hashpw(input_password,bcrypt.gensalt()).decode('utf-8')
    user.save()
    return Response({'massage':"password change success"},status=200)

@api_view(['GET'])
def lookup(request):
    user = ST_User.objects.all()
    response = []
    for i in user:
        response.append(i.user_email)
    print(response)
    return Response(response,status=200)

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
        return Response({"message" : "user create success"},status=200)
    
    @login_check
    def get(self,request):
        serializer = ST_UserSerializer(request.user)
        return Response(serializer.data,status=200)
    
    @login_check
    def put(self,request):
        serializer =ST_UserSerializer(request.user)
        print(serializer.data)
        data = request.data
        if serializer.data['user_email'] != data['user_email']:
            request.user.user_email = data['user_email']
        if not bcrypt.checkpw(data['user_password'].encode('utf-8'),serializer.data['user_password'].encode('utf-8')):
            hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            request.user.user_password= hashed_password
        if serializer.data['user_nickname'] != data['user_nickname']:
            request.user.user_nickname=data['user_nickname']
        request.user.save()
        
        return Response({'message':'success'},status=200)
    
    @login_check
    def delete(self,request):
        user_email = request.user.user_email
        request.user.delete()
        return Response({'message': user_email+" is delete success"},status=200)



class UserPresentationAPI(APIView):
    """
        발표연습 생성,조회
        
        ---
        ## 내용
        - 발표연습 생성 : 유저의 발표연습 생성 로그인토큰, presentation_title, presentation_time, presentation_date 필요
        - 발표연습 조회 : 유저의 전체 발표연습 조회 로그인토큰 필요
    """
    @login_check
    def post(self,request):
        data = request.data
        if not (data['presentation_title'] and data['presentation_time'] and data['presentation_date']) :
            return Response({'massage': 'missing parameter'},status=400)

        presentataion = Presentation(user_id = request.user,
                    presentation_title = data['presentation_title'],
                    presentation_time = data['presentation_time'],
                    presentation_date = data['presentation_date']
        )
        presentataion.save()
        return Response({'massage': 'create presentation', 'presentation_id' : presentataion.presentation_id },status=200)

    @login_check
    def get(self,request):
        queryset = Presentation.objects.filter(user_id = request.user)
        response = []
        for q in queryset:
            response.append(PresentationSerializer(q).data)
        return Response(response,status=200)



class PresentationAPI(APIView):
    """
        특정 발표연습 조회,수정,삭제 API
        
        ---
        ## 내용
        - 발표연습 조회 : url뒤의 <int:pk> 로 특정 발표연습 판별하여 특정 발표연습 세부정보 응답
        - 발표연습 수정 : url뒤의 <int:pk> 로 특정 발표연습 수정 로그인토큰, presentation_title, presentation_time, presentation_date, presentation_ex_dupword, presentation_ex_improper 필요
        - 발표연습 삭제 : url뒤의 <int:pk> 로 특정 발표연습 삭제 로그인토큰 필요
    """
    def get(self,request,pk):
        try:
            queryset = Presentation.objects.get(pk=pk)
        except Presentation.DoesNotExist:
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        serializer = PresentationSerializer(queryset)
        return Response(serializer.data,status=200)
    
    @login_check
    def put(self,request,pk):
        try:
            queryset = Presentation.objects.get(pk=pk)
        except Presentation.DoesNotExist:
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if queryset.user_id != request.user:
            return Response({'massage':'DO NOT LOGIN ERROR'},status=400)
        data = request.data
        print(data)
        queryset.presentation_title = data['presentation_title']
        queryset.presentation_time = data['presentation_time']
        queryset.presentation_date = data['presentation_date']
        queryset.presentation_ex_dupword = data['presentation_ex_dupword']
        queryset.presentation_ex_improper = data['presentation_ex_improper']
        try:
            queryset.save()
        except Exception as e:
            return Response(e,status=400)

        return Response({'massage':queryset.presentation_title+' presenatataion update success'},status=200)

    @login_check
    def delete(self,request,pk):
        try:
            queryset = Presentation.objects.get(pk=pk)
            presentation_title = queryset.presentation_title
            queryset.delete()
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        
        return Response({'massage': presentation_title +' is deleted'},status=200)


class KeyWordAPI(APIView):
    """
    인풋
    {
        "1" : "자장면, 볶음밥, 탕수육",
        "2" : "어쩌고, 저쩌고",
        "4" : "스트링, 스트링"        
    }
    
    """

    @login_check
    def post(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        data =request.data
        for key,val in data.items():
            try:
                int(key)
            except ValueError :
                return Response({'massage':'key is not integer error'},status=400)
            if len(val) and (not KeyWord.objects.filter(presentation_id =presentation, keyword_page=int(key)).exists()):
                KeyWord(presentation_id=presentation,keyword_page=int(key),keyword_contents=val).save()
                print(key,val)
        return Response({'massage':'create keyword success'},status=200)
    
    @login_check
    def get(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        queryset = KeyWord.objects.filter(presentation_id=presentation).order_by('keyword_page')
        serializer = KeyWordSerializer(queryset,many=True)
        return Response(serializer.data,status=200)

    @login_check
    def put(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        data = request.data
        for key,val in data.items():
            try:
                int(key)
            except ValueError :
                return Response({'massage':'key is not integer error'},status=400)
            keyword = KeyWord.objects.filter(presentation_id = presentation, keyword_page=int(key))
            if len(val) and keyword.exists():
                keyword.update(keyword_contents=val)
            elif len(val) :
                KeyWord(presentation_id=presentation,keyword_page=int(key),keyword_contents=val).save()
            print(key,val)
        return Response({'massage':'update keyword success'},status=200)

    @login_check
    def delete(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        queryset = KeyWord.objects.filter(presentation_id=presentation)
        queryset.delete()
        return Response({'massage':'keyword delete success'},status=200)



class ScriptAPI(APIView):
    """
    인풋
    {
        "1" : "대본1",
        "2" : "대본2",
        "4" : "대본3"        
    }
    
    """

    @login_check
    def post(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        data =request.data
        for key,val in data.items():
            try:
                int(key)
            except ValueError :
                return Response({'massage':'key is not integer error'},status=400)
            if len(val) and (not Script.objects.filter(presentation_id=presentation,keyword_page=int(key)).exists()):
                Script(presentation_id=presentation,keyword_page=int(key),keyword_contents=val).save()
                print(key,val)
        return Response({'massage':'create keyword success'},status=200)
    
    @login_check
    def get(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        queryset = Script.objects.filter(presentation_id=presentation).order_by('keyword_page')
        serializer = KeyWordSerializer(queryset,many=True)
        return Response(serializer.data,status=200)

    @login_check
    def put(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)

        data = request.data
        for key,val in data.items():
            try:
                int(key)
            except ValueError :
                return Response({'massage':'key is not integer error'},status=400)
            keyword = Script.objects.filter(presentation_id=presentation,keyword_page=int(key))
            if len(val) and keyword.exists():
                keyword.update(keyword_contents=val)
            elif len(val) :
                Script(presentation_id=presentation,keyword_page=int(key),keyword_contents=val).save()
            print(key,val)
        return Response({'massage':'update keyword success'},status=200)

    @login_check
    def delete(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'massage':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'massage': 'DONT ACEESS PRESENTATION'},status=400)
        queryset = Script.objects.filter(presentation_id=presentation)
        queryset.delete()
        return Response({'massage':'keyword delete success'},status=200)