from typing import Any
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

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
