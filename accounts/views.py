from typing import Any, Type

from rest_framework import generics, status, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.request import Request


from django.contrib.auth import login

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserLoginSerializer,
    UserUpdateSerializers,
    ChangePasswordSerializers,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        # try:
        #     serialized_user = UserProfileSerializer(user)
        #     print("Serialized user data:", serialized_user.data)  # Для отладки
        # except Exception as e:
        #     print("Error in UserProfileSerializer:", str(e))  # Для отладки
        #     raise

        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),  # type: ignore[attr-defined]
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        login(request, user)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),  # type: ignore[attr-defined]
                "message": "user logged successfully",
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return UserUpdateSerializers

        return UserProfileSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Password changed successfully",
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request: Request) -> Response:
    try:
        refresh_token = RefreshToken.for_user("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {
                "error": "Invalid toke",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from models import Accounts
# from serializers import (
#     AccountsSerializer,
#     AccountsCreateSerializer,
#     AccountsUpdateSerializer,
# )


# class AccountsListCreateView(generics.ListCreateAPIView):
#     queryset = Accounts.objects.all()

#     def get_serializer_class(self) -> AccountsSerializer:
#         if self.request.method == "POST":
#             return AccountsCreateSerializer

#         return AccountsSerializer

#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         # Обрабатывает GET запрос для получения списка заметок
#         return super().get(request, *args, **kwargs)


# class AccountsDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Accounts.objects.all()

#     def get_serializer_class(self) -> AccountsSerializer:
#         if self.request.method in ["PUT", "PATCH"]:
#             return AccountsUpdateSerializer

#         return AccountsSerializer

#     def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.date, partial=partial)

#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response(serializer.data)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(
#             {"message": "Заметка успешно удалена"},
#             status=status.HTTP_204_NO_CONTENT,
#         )
