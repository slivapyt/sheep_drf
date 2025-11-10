from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from accounts.models import User

# from models import Accounts
# from django.utils.html import escape


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        )

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."},
            )

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> User:
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        email = attrs.get("email")
        password = attrs.get("password")

        if not (email and password):
            raise serializers.ValidationError("Must include 'email' and 'password' ")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            raise serializers.ValidationError(
                {"Invalid email or password."},
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"User account is disabled."},
            )

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "avatar",
            "bio",
            "created_at",
            "updated_at",
            "posts_count",
            "comments_count",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    full_name = serializers.ReadOnlyField()
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_posts_count(self, obj: User) -> int:
        try:
            return obj.posts.count()
        except AttributeError:
            return 0

    def get_comments_count(self, obj: User) -> int:
        try:
            return obj.comments.count()
        except AttributeError:
            return 0


class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "bio")

    def update(self, instance: User, validated_data: User) -> User:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save
        return instance


class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
    )
    new_password_confirm = serializers.Serializer(required=True)

    def save(self) -> User:
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user

    def validate_old_password(self, value: User) -> User:
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")

        return value

    def validate(self, attrs: User) -> User:
        if attrs("new_password") != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"'new_password': 'Password fields didn't match.'"},
            )

        return attrs


# class AccountsSerializer(serializers.ModelSerializer):
#     class Meta:
#         models = Accounts
#         fields = ["id", "title", "content", "created_at", "updated_at"]
#         read_only_fields = ["id", "created_at", "updated_at"]

#     def validate_title(self, value: str) -> str:
#         if not value.strip():
#             raise serializers.ValidationError("Заголовок не может быть пустым")

#         return escape(value.strip())

#     def validate_content(self, value: str) -> str:
#         if not value.strip():
#             raise serializers.ValidationError("Содержание не может быть пустым")

#         return escape(value.strip())


# class AccountsCreateSerializer(AccountsSerializer):

#     pass


# class AccountsUpdateSerializer(AccountsSerializer):
#     # Для обновления
#     title = serializers.CharField(required=False)
#     content = serializers.CharField(required=False)
