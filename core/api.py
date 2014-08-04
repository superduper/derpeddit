from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import authentication

from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import LoginSerializer, SingUpSerializer, ProfileSerializer


class AuthProfileView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request):
        if request.user.is_anonymous():
            return Response(status=403)
        return Response(ProfileSerializer(request.user).data)


class LoginView(APIView):

    def post(self, request, format=None):
        login_serializer = LoginSerializer(data=request.DATA)
        if login_serializer.is_valid():
            user = authenticate(**login_serializer.data)
            if user:
                if user.is_active:
                    login(request, user)
                    return Response(LoginSerializer(user).data)
                else:
                    return Response({"non_field_errors":"User is inactive"}, status=403)
            else:
                return Response({"non_field_errors":"Login and password do not match"}, status=401)
        else:
            return Response(login_serializer.errors, status=400)


class LogoutView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request, format=None):
        logout(request)
        return Response()


class SignUpView(APIView):

    def post(self, request, format=None):
        # validate
        signup_serializer = SingUpSerializer(data=request.DATA)
        if not signup_serializer.is_valid():
            return Response(signup_serializer.errors, status=400)
        # create user
        User.objects.create_user(**signup_serializer.data)

        # authenticate
        creds = dict(
            username=signup_serializer.data["username"],
            password=signup_serializer.data["password"],
        )
        user = authenticate(**creds)
        login(request, user)
        # return profile
        profile_serializer = ProfileSerializer(instance=user)
        return Response(profile_serializer.data, status=201)