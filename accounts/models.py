from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


# class Accounts(models.Model):
#     class Meta:
#         verbose_name = "Заметка"
#         verbose_name_plural = "Заметки"
#         ordering = ["-created_at"]

#     title = models.CharField(
#         max_length=200,
#         verbose_name="Заголовки",
#         help_text="Введите заголовок заметки",
#     )
#     content = models.TextField(
#         validators=[MaxValueValidator(10000)],
#         verbose_name="Содержание",
#         help_text="введите содержание заметки",
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="Дата создания",
#     )
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

#     def __str__(self) -> str:
#         return self.title[:50]


class User(AbstractUser):
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
