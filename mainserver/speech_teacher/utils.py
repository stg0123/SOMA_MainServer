from mainserver.settings import SECRET_KEY
import jwt
from rest_framework.response import Response
from .models import ST_User
def login_check(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            access_token = request._request.headers['Authorization']
            payload = jwt.decode(access_token,SECRET_KEY,algorithms='HS256')
            request.user = ST_User.objects.get(user_id=payload['user_id'])
            print(payload)
            
        except jwt.exceptions.DecodeError:
            return Response({'massage':'INVALID TOKEN'},status=400)
        
        except ST_User.DoesNotExist:
            return Response({'massage':'INVALID USER'},status=400)
        
        return func(self,request,*args,**kwargs)

    return wrapper
