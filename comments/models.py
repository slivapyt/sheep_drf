from django.db import models

from config import settings


class Comment(models.Model):
    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post", "-created_at"]),
            models.Index(fields=["author", "-created_at"]),
            models.Index(fields=["parent", "-created_at"]),
        ]

    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(
        "main.Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.post.title}"

    @property
    def replies_count(self) -> str:
        return self.replies.filter(is_active=True).cont()

    @property
    def is_reply(self) -> bool:
        return self.parent is not None
