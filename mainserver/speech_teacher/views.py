from django.core.exceptions import ValidationError
from django.db.models import query
from django.http.response import JsonResponse
from mainserver.settings import SECRET_KEY
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from django.core.cache import cache
from .models import *
from .serializers import *
from .utils import login_check
import requests
import os
import bcrypt
import re
import jwt


@api_view(['GET'])
def HelloWorld(request):
    res = "helloworld kospeech (MSS)"
    return Response(res,status=200)

@api_view(['POST'])
def LoginAPI(request):
    data = request.data
    try:
        input_email =data["user_email"]
        input_password = data["user_password"].encode('utf-8')
    except Exception :
        return Response({'message':'KEY_ERROR'},status=400)
    
    try:
        user_ck = ST_User.objects.get(user_email = input_email)
    except Exception:
        return Response({'message':'INVALID_USER'},status=400)

    if bcrypt.checkpw(input_password,user_ck.user_password.encode('utf-8')):
        access_token = jwt.encode({'user_id':user_ck.user_id},SECRET_KEY,algorithm='HS256')
        print(access_token)
        print(jwt.decode(access_token,SECRET_KEY,algorithms='HS256'))
        return Response({'message':'success', 'access_token':access_token},status=200)
    
    return Response({"message" : "INVALID_PASSWORD"},status=400)

@api_view(['POST'])
def changepw(request):
    data = request.data
    try:
        input_email = data['user_email']
        input_password = data['user_password'].encode('utf-8')
    except Exception:
        return Response({'message': 'KEY_ERROR'},status=400)
    user = ST_User.objects.get(user_email = input_email)
    user.user_password= bcrypt.hashpw(input_password,bcrypt.gensalt()).decode('utf-8')
    user.save()
    return Response({'message':"password change success"},status=200)

@api_view(['GET'])
def lookup(request):
    users =ST_User.objects.all().values('user_id','user_email','user_nickname','user_create_date')
    return Response(list(users),status=200)

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
        if data['user_password']!="" and not bcrypt.checkpw(data['user_password'].encode('utf-8'),serializer.data['user_password'].encode('utf-8')):
            hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            request.user.user_password= hashed_password
        if data['user_nickname']!="" and serializer.data['user_nickname'] != data['user_nickname']:
            request.user.user_nickname=data['user_nickname']
        request.user.save()
        
        return Response({'message':'updatesuccess'},status=200)
    
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
        if ("presentation_title" not in data) or ("presentation_time" not in data) or ("presentation_date" not in data) :
            return Response({'message': 'missing parameter'},status=400)
        try:
            presentataion = Presentation(user_id = request.user,
                        presentation_title = data['presentation_title'],
                        presentation_time = data['presentation_time'],                               
                        presentation_date = data['presentation_date']
            )
            presentataion.save()
        except ValidationError as e:
            return Response({'message': 'time is not valid(HH:MM)'},status=400)
        return Response({'message': 'create presentation', 'presentation_id' : presentataion.presentation_id },status=200)

    @login_check
    def get(self,request):
        queryset = Presentation.objects.filter(user_id = request.user)

        queryset_result = PresentationResult.objects.filter(user_id = request.user.user_id)
        response = PresentationSerializer(queryset,many=True).data # json 형태로 바꿔줌
        i=0
        for q in queryset:
            presentation_result_info = 0
            for qq in queryset_result:
                if q.presentation_id == qq.presentation_id.presentation_id:
                    presentation_result_info+=1
            response[i]["presentation_result_info"]=presentation_result_info
            i+=1
        
        print(response)
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
    @login_check
    def get(self,request,pk):
        try:
            queryset = Presentation.objects.prefetch_related('presentation_file').get(presentation_id=pk)
        except Presentation.DoesNotExist:
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        serializer = PresentationSerializer(queryset).data
        try:
            presentation_file = queryset.presentation_file.get()
        except PresentationFile.DoesNotExist :
            return Response(serializer,status=200)

        serializer["presentation_file_url"]=presentation_file.file.url
        print(serializer)
        return Response(serializer,status=200)
    
    @login_check
    def put(self,request,pk):
        try:
            queryset = Presentation.objects.get(pk=pk)
        except Presentation.DoesNotExist:
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if queryset.user_id != request.user:
            return Response({'message':'DO NOT LOGIN ERROR'},status=400)
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

        return Response({'message':queryset.presentation_title+' presenatataion update success'},status=200)

    @login_check
    def delete(self,request,pk):
        try:
            queryset = Presentation.objects.get(pk=pk)
            presentation_title = queryset.presentation_title
            queryset.delete()
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        
        return Response({'message': presentation_title +' is deleted'},status=200)


class KeyWordAPI(APIView):
    """
    인풋
    {
        "0" : "자장면, 볶음밥, 탕수육",
        "1" : "어쩌고, 저쩌고",
        "3" : "스트링, 스트링"        
    }
    
    """

    @login_check
    def post(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        data =request.data
        print(data)
        for key,val in data.items():
            if len(val) and isinstance(key,str):
                KeyWord(presentation_id=presentation,keyword_page=int(key),keyword_contents=val).save()
        return Response({'message':'create keyword success'},status=200)
    
    @login_check
    def get(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        queryset = KeyWord.objects.filter(presentation_id=presentation).order_by('keyword_page')
        serializer = KeyWordSerializer(queryset,many=True)
        return Response(serializer.data,status=200)

    @login_check
    def put(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        data = request.data
        for key,val in data.items():
            try:
                int(key)
            except ValueError :
                return Response({'message':'key is not integer error'},status=400)
            keyword = KeyWord.objects.filter(presentation_id = presentation, keyword_page=int(key))
            if len(val) and keyword.exists():
                keyword.update(keyword_contents=val)
            elif len(val) :
                KeyWord(presentation_id=presentation,keyword_page=int(key),keyword_contents=val).save()
            print(key,val)
        return Response({'message':'update keyword success'},status=200)

    @login_check
    def delete(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        queryset = KeyWord.objects.filter(presentation_id=presentation)
        queryset.delete()
        return Response({'message':'keyword delete success'},status=200)



class ScriptAPI(APIView):
    """
    인풋
    {
        "0" : "대본1",
        "1" : "대본2",
        "4" : "대본3"        
    }
    
    """

    @login_check
    def post(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        data =request.data
        print(data)
        for key,val in data.items():
            if len(val) and isinstance(key,str):
                Script(presentation_id=presentation,script_page=int(key),script_contents=val).save()
        return Response({'message':'create keyword success'},status=200)
    
    @login_check
    def get(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        queryset = Script.objects.filter(presentation_id=presentation).order_by('script_page')
        serializer = ScriptSerializer(queryset,many=True)
        return Response(serializer.data,status=200)

    @login_check
    def put(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)

        data = request.data
        for key,val in data.items():
            try:
                int(key)
            except ValueError :
                return Response({'message':'key is not integer error'},status=400)
            script = Script.objects.filter(presentation_id=presentation,script_page=int(key))
            if len(val) and script.exists():
                script.update(script_contents=val)
            elif len(val) :
                Script(presentation_id=presentation,script_page=int(key),script_contents=val).save()
            print(key,val)
        return Response({'message':'update script success'},status=200)

    @login_check
    def delete(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message':'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)
        queryset = Script.objects.filter(presentation_id=presentation)
        queryset.delete()
        return Response({'message':'keyword delete success'},status=200)

class AllFileAPI(APIView):
    """
        전체 파일 보기
        get
    """
    @login_check
    def get(self,request):
        queryset = PresentationFile.objects.filter(user_id=request.user.user_id)
        response = []
        for i in queryset:
            response.append({"file_id":i.presentationfile_id ,"presentation_id":i.presentation_id.presentation_id,"file_name" : i.file_name , "file_url" : i.file.url })
        return Response(response,status=200)


class PresentationFileAPI(APIView):
    """
    인풋
    {
       "file" : file.확장자
    }
    """
    @login_check
    def post(self,request,presentation_id):
        if "file" not in request.FILES :
            return Response({'message':'missing file error'},status=400)
        elif os.path.splitext(request.FILES['file'].name)[1]!='.pdf' :
            return Response({'message':'only possible file extenstion is PDF'},status=400)
        
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)
        

        if PresentationFile.objects.filter(presentation_id=presentation).exists():
            return Response({'message': 'already file exists error'},status=400)

        file =PresentationFile(presentation_id = presentation,user_id = request.user.user_id,file_name = request.FILES['file'].name,file = request.FILES['file'])
        file.save()
        return Response({'message': 'upload file success','file_id' : file.presentationfile_id},status=200)

    @login_check
    def get(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(presentation_id=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)
        
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)
        
        try:
            file= PresentationFile.objects.get(presentation_id=presentation)
        except PresentationFile.DoesNotExist :
            return Response({'message':'file is not exist error'},status=400)


        return Response({"file_id":file.presentationfile_id ,"presentation_id":file.presentation_id.presentation_id ,"file_name" : file.file_name, "file_url" : file.file.url },status=200)

    @login_check
    def put(self,request,presentation_id):
        if  "file" not in request.FILES :
            return Response({'message':'missing file error'},status=400)
        elif os.path.splitext(request.FILES['file'].name)[1]!='.pdf' :
            return Response({'message':'only possible file extenstion is PDF'})

        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)
        
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)
        
        try:
            file= PresentationFile.objects.get(presentation_id=presentation)
        except PresentationFile.DoesNotExist :
            return Response({'message':'file is not exist error'},status=400)
        file.file_name=request.FILES['file'].name
        file.file=request.FILES['file']
        file.save()
        return Response({'message':str(presentation_id)+" presentation file update success"},status=200)

    @login_check
    def delete(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)
        
        if presentation.user_id.user_id != request.user.user_id:
            return Response({'message': 'DONT ACEESS PRESENTATION'},status=400)
        
        PresentationFile.objects.filter(presentation_id=presentation).delete()
        return Response({'message':str(presentation_id)+' presentation file is deleted'},status=200)

class PresentationResultAPI(APIView):
    """
    결과 생성
    -연습의 결과 생성
    입력
    {
        "audio_file": file
        "presentation_result_time": int
    }
    결과 조회
    - 모든 결과의 결과id,연습번호,생성일을 반환 > 이걸가지고 디테일에서 찾아오면됨 
    결과 삭제
    - 연습의 모든 결과 삭제
    """
    @login_check
    def post(self,request,presentation_id):
        data = request.data
        time = data['presentation_result_time']
        print(time)
        if "audio_file" not in request.FILES :
            return Response({'message':'missing file error'},status=400)
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)

        try:
            res = requests.post('http://10.1.205.38:8000/analysis',files ={"audio_file":request.FILES["audio_file"]}) 
        except Exception :
            return Response({'message':'error'},status=400)
        res_data = res.json()
        if res.status_code == 400:
            return Response(res_data,status=400)
        print(res_data)
        PresentationResult(presentation_id = presentation, user_id = request.user.user_id, presentation_result_audiofile = request.FILES["audio_file"],
                            presentation_result_time=int(time), presentation_result = res_data).save()
        
        return Response(res_data,status=200)

    @login_check
    def get(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)
        queryset = PresentationResult.objects.filter(presentation_id=presentation)
        response = []
        for q in queryset:
            response.append({"presentation_result_id":q.presentation_result_id ,"presentation_result":q.presentation_result,"audiofile_url": q.presentation_result_audiofile.url,
            "presentation_result_time":q.presentation_result_time ,"presentation_result_date":q.presentation_result_date})
        return Response(response,status=200)
    
    @login_check
    def delete(self,request,presentation_id):
        try:
            presentation = Presentation.objects.get(pk=presentation_id)
        except Presentation.DoesNotExist :
            return Response({'message': 'INVALID PRESENTATION_ID'},status=400)
        PresentationResult.objects.filter(presentation_id=presentation).delete()
        return Response({'message':str(presentation_id)+' result is all deleted'},status=200)
            
        
class PresentationResultDetailAPI(APIView):
    """
    프레젠테이션 결과 상세 정보 조회
    get - 결과 상세 정보 조회
    put - 결과 상세 정보 수정 (필요없을 듯)
    delete -결과 삭제
    """
    @login_check
    def get(self,request,presentation_result_id):
        try:
            queryset = PresentationResult.objects.get(pk=presentation_result_id)
        except PresentationResult.DoesNotExist :
            return Response({'message':'not found that result error'},status=400)
        response = PresentationResultSerializer(queryset).data
        response['presentation_result_audiofile']=queryset.presentation_result_audiofile.url
        return Response(response,status=200)
    
    @login_check
    def delete(self,request,presentation_result_id):
        try:
            queryset = PresentationResult.objects.get(pk=presentation_result_id)
        except PresentationResult.DoesNotExist :
            return Response({'message':'not found that result error'},status=400)
        queryset.delete()
        return Response({'message':str(presentation_result_id)+' presentation_result is deleted'},status=200)
        

class TestAPI(APIView):
    def post(self,request):
        data = request.data
        TESTDB(testdb_num =int(data['testdb_num']),testdb_string = data['testdb_string']).save()
        return Response({'message':'create success'},status=200)

    def get(self,request):
        queryset = TESTDB.objects.all()
        serializer = TESTDBSerializer(queryset,many=True)
        return Response(serializer.data,status=200)

@api_view(['GET'])
def TESTgetAPI(request,testdb_id):
    queryset = TESTDB.objects.get(testdb_id=testdb_id)
    serializer = TESTDBSerializer(queryset)
    return Response(serializer.data,status=200)



class KnowhowAPI(APIView):
    """
        노하우 생성, 조회
        {
            'knowhow_img' : file,
            'knowhow_title' : str,
            'knowhow_contents' : str
        }
    """
    def post(self,request):
        data = request.data
        if "knowhow_img" not in request.FILES :
            return Response({'message':'missing file error'},status=400)
        
        Knowhow(knowhow_title=data['knowhow_title'],knowhow_img = request.FILES["knowhow_img"],knowhow_contents=data['knowhow_contents']).save()
        return Response({'message':'knowhow create success'},status=200)
        
    def get(self,request):
        queryset = Knowhow.objects.all()
        res = []
        for q in queryset:
            res.append({'knowhow_title':q.knowhow_title , 'knowhow_img_url':q.knowhow_img.url ,'knowhow_contents':q.knowhow_contents })
        return Response(res,status=200)

    def delete(self,request):
        data = request.data
        if "knowhow_id" not in data:
            return Response({'message':'missing knowhow_id'},status=400)
        queryset = Knowhow.objects.filter(knowhow_id =data['knowhow_id'])
        queryset.delete()
        return Response({'message':'knowhow delete success'},status=200)
        
