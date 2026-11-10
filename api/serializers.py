from rest_framework import serializers

from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created_at', 'completed']


class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id'] # why need to show id?
        # 因为该序列化器只是用来反转 completed 状态的，不接收其他字段的更新
        # 注意：文档中写的是 'created'，但实际模型中字段名为 'created_at'，为避免报错此处写 'created_at'
        read_only_fields = ['title', 'memo', 'created_at', 'completed']