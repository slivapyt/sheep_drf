from typing import Any, Optional
from rest_framework import serializers
from django.utils.text import slugify
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "posts_count", "created_at"]
        read_only_fields = ["slug", "created_at"]

    posts_count = serializers.SerializerMethodField()

    def get_posts_count(self, obj: Any) -> int:
        return obj.posts.filter(status="published").count()

    def create(self, validated_data: dict[str, Any]) -> Any:
        validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "image",
            "category",
            "author",
            "status",
            "created_at",
            "updated_at",
            "views_count",
            "comments_count",
        ]
        read_only_fields = ["slug", "author", "views_count"]

    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    comments_count = serializers.ReadOnlyField()

    def to_representation(self, instance: Any) -> dict[str, Any]:
        data = super().to_representation(instance)
        if len(data["content"]) > 200:
            data["content"] = data["content"][:200] + "..."

        return data


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "image",
            "category",
            "category_info",
            "author",
            "author_info",
            "status",
            "created_at",
            "updated_at",
            "views_count",
            "comments_count",
        ]
        read_only_fields = ["slug", "author", "views_count"]

    author_info = serializers.SerializerMethodField()
    category_info = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()

    def get_author_info(self, obj: Any) -> dict[str, Any]:
        author = obj.author
        return {
            "id": author.id,
            "username": author.username,
            "full_name": author.full_name,
            "avatar": author.avatar.url if author.avatar else None,
        }

    def get_category_info(self, obj: Any) -> Optional[dict[str, Any]]:
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "slug": obj.category.slug,
            }

        return None


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "image", "category", "status"]

    def create(self, validated_data: dict[str, Any]) -> Any:
        validated_data["author"] = self.context["request"].user
        validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)

    def update(self, instance: Any, validated_data: dict[str, Any]) -> Any:
        if "title" in validated_data:
            validated_data["slug"] = slugify(validated_data["title"])

        return super().update(instance, validated_data)
