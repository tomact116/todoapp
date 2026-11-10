from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo

# Practical 4 新增导入
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Practical 5 新增：导入 authenticate 用于验证用户
from django.contrib.auth import authenticate

# Create your views here.

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


# Practical 4 新增：用于切换 Todo 完成状态的视图
class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        # 在更新发生前，将 completed 的布尔值取反（invert）
        # i.e. if its true, set to false, if false, set to true.
        serializer.instance.completed = not (serializer.instance.completed)
        serializer.save()


# Practical 4 新增：用户注册视图
@csrf_exempt  # 因为 POST 请求来自不同域（前端域）且没有 CSRF token，所以需要 csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)  # data is a dictionary
            # 从字典中提取用户输入并创建用户
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            # 用户保存后，创建 Token 对象
            token = Token.objects.create(user=user)
            return JsonResponse(data={'token': str(token)}, status=201)
        except IntegrityError:
            # 如果用户名重复导致报错，返回 400 状态码及错误信息
            return JsonResponse(data={'error': 'username taken. choose another username'}, status=400)


# Practical 5 新增：用户登录视图
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # 提取用户输入的用户名和密码并验证
        user = authenticate(
            request,
            username=data['username'],
            password=data['password']
        )
        
        if user is None:
            # 验证失败，返回 400 状态码
            return JsonResponse(
                data={'error': 'unable to login. check username and password'},
                status=400
            )
        else:
            # 验证成功，获取 user token
            try:
                token = Token.objects.get(user=user)
            except:
                # if token not in db, create a new one (如果数据库中无 token，则新建一个)
                token = Token.objects.create(user=user)
            
            return JsonResponse(data={'token': str(token)}, status=201)