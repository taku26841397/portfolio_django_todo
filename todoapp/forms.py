from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        #使用するモデルをTodoに限定
        model = Todo
        
        fields = ['title','memo','completed']
        
        #ラベルのカスタマイズ
        labels = {
            'title':'タスク名',
            'memo':'詳細メモ',
            'completed':'完了済み',
        }