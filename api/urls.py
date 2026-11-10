from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoListCreate.as_view()), 
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()), 
    # Practical 4 新增：处理 complete 操作的路由
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
    # Practical 4 新增：用户注册路由
    path('signup/', views.signup),
    # Practical 5 新增：用户登录并获取 Token 的路由
    path('login/', views.login),
]