# todo/todo_api/urls.py : API urls.py
from django.urls import path, include
from .views import (
    TodoListApi,
)

urlpatterns = [
    path('api', TodoListApi.as_view()),
]