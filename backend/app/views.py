from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .serializers import UserRegisterSerializer, UserLoginSerializer


class RegisterView(APIView):

    @extend_schema(
        summary="register",
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer},
    )
    def post(self, request):
        print(request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserRegisterSerializer(user)
            return Response(
                {
                    'message': 'register success',
                    'user': user_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            errors = serializer.errors
            return Response(
                {
                    'message': 'Bad request',
                    'errors': errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)
        else:
            errors = serializer.errors
            return Response(
                {
                    "message": "Bad Request.", 
                    "errors": errors
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user:
            refresh = RefreshToken.for_user(user)
            payload = {"user_id": user.id, "username": user.username}
            access_token = refresh.access_token
            access_token["payload"] = payload

            return Response(
                {
                    "message": "User logged in successfully.",
                    "access_token": str(access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

