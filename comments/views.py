from typing import Type
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, permissions, serializers, filters
from rest_framework.response import Response
from rest_framework.request import Request

from django.db.models import QuerySet
from .models import Comment
from .serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    CommentDetailSerializer,
)
from .permissions import IsAuthorOrReadOnly
from main.models import Post
from rest_framework.decorators import api_view, permission_classes


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["post", "author", "parent"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Comment]:
        return Comment.objects.filter(is_active=True).select_related(
            "author",
            "post",
            "parent",
        )

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.request.method == "POST":
            return CommentCreateSerializer

        return CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(is_active=True).select_related("author", "post")
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.request.method in ["PUT", "PATCH"]:
            return CommentUpdateSerializer

        return CommentDetailSerializer


class MyCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["post", "parent", "is_active"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Comment]:
        return Comment.objects.filter(author=self.request.user).select_related(
            "post",
            "parent",
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def post_comments(request: Request, post_id: int) -> Response:
    post = get_object_or_404(Post, id=post_id, status="published")
    comments = (
        Comment.objects.filter(post=post, parent=None, is_active=True)
        .select_related("author")
        .prefetch_related("replies_author")
        .order_by("-created_at")
    )
    serializer = CommentDetailSerializer(
        comments,
        many=True,
        context={"request": request},
    )
    return Response(
        {
            "post": {"id": post.id, "title": post.title, "slug": post.slug},
            "comments": serializer.data,
            "comment_count": post.comments.filter(is_active=True).count(),
        },
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def comment_replies(request: Request, comment_id: int) -> Response:
    parent_comment = get_object_or_404(Comment, id=comment_id, is_active=True)

    replies = (
        Comment.objects.filter(parent=parent_comment, is_active=True)
        .select_related("author")
        .order_by("created_at")
    )

    serializer = CommentSerializer(replies, many=True, context={"request": request})
    return Response(
        {
            "parent_comment": CommentSerializer(
                parent_comment,
                context={"request": request},
            ).data,
            "replies": serializer.data,
            "replies_count": replies.count(),
        },
    )
