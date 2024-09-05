from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework import views, permissions, status
from rest_framework.response import Response

from api.models import Interview
from base.management.auth_checker import check_authentication

from .modules.notify import notify_user
from .modules.authentication import Login, SignUp

@api_view(['GET'])
def baseAPi(request):
    return Response({'message': 'Hello, World!'})

class userCreation(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        singup = SignUp()
        try:
            otp = request.GET.get('otp')
            email = request.GET.get('email')
            password = request.GET.get('password')
            if password and email:
                req = singup.add_password(email=email, password=password)
                return Response({"message": req})
            elif otp and email:
                req = singup.signup_otp(email=email, otp=otp)
                return Response({"message": req})
            elif email:
                req = singup.signup_base(email=email)
                print(req)
                return Response({"message": req})
            else:
                print("else?")
                return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        login = Login()
        try:
            email = request.data['email']
            password = request.data['password']
            print(email, password)
            if email and password:
                req = login.login_base(email=email, password=password)
                return Response({"message": req})
            else:
                return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)