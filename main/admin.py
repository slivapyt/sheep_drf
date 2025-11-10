from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Post
from django.db.models import QuerySet
from django.http import HttpRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "posts_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)

    def posts_count(self, obj: Category) -> str:  # noqa: CCE001
        return obj.post.count()

    posts_count.short_description = "Post Count"  # type: ignore[attr-defined]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "views_count",
        "comments_count",
        "created_at",
    )
    list_filter = ("status", "category", "created_at", "updated_at")
    search_fields = ("title", "count", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "views_count")
    raw_id_fields = ("author",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "content", "image")}),
        ("Meta", {"fields": ("category", "author", "status")}),
        (
            "Statistics",
            {
                "fields": ("views_count", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def comments_count(self, obj: Post) -> str:  # noqa: CCE001
        return obj.comments.count()

    comments_count.short_description = "Comments"  # type: ignore[attr-defined]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Post]:  # noqa: CCE001
        return super().get_queryset(request).select_related("author", "category")
