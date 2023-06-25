# todo/todo_api/urls.py : API urls.py
from django.urls import path, include
from .views import (
    TodoListApi, TodoDetail
)

urlpatterns = [
    path('api', TodoListApi.as_view()),
    path('api/<int:todo_id>/', TodoDetail.as_view()),
]