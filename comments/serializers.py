from typing import Any, List
from rest_framework import serializers

from main.models import Post
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "author_info",
            "parent",
            "is_active",
            "replies_count",
            "is_reply",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "is_active"]

    author_info = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    is_reply = serializers.ReadOnlyField()

    def get_author_info(self, obj: Any) -> dict[str, Any]:
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "full_name": obj.author.full_name,
            "avatar": obj.author.avatar.url if obj.author.avatar else None,
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "parent", "content"]

    def validate_post(self, value: Any) -> Any:
        if not Post.objects.filter(id=value.id, status="published").exists():
            raise serializers.ValidationError("Post not found")

        return value

    def validate_parent(self, value: Any) -> Any:
        if value:
            post_data = self.initial_data.get("post")
            if post_data:
                if value.post.id != int(post_data):
                    raise serializers.ValidationError(
                        "Parent comment must belong to the same post",
                    )

        return value

    def create(self, validated_data: dict[str, Any]) -> Any:
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["content"]


class CommentDetailSerializer(CommentSerializer):
    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ["replies"]

    replies = serializers.SerializerMethodField()

    def get_replies(self, obj: Any) -> List[dict]:
        if obj.parent is None:
            replies = obj.replies.filter(is_active=True).order_by("create_at")
            return CommentSerializer(replies, many=True, context=self.context).data

        return []
