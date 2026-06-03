from django.db import models
# import pandas as pd
# from django_pandas.io import read_frame


class Todo(models.Model):
    #タイトル：最大３０文字の文字列フィールド
    title = models.CharField(max_length=30)
    
    #メモ：長文テキストフィールド（空でもOK）
    memo = models.TextField(null=True, blank=True)

    #完了フラグ：真偽値（Boolean)フィールド（デフォルトは未完了）
    completed = models.BooleanField(default=False)
    
    #作成日時：日付フィールド（自動的に現在時刻が設定される）
    created = models.DateTimeField(auto_now_add=True)
    
    #更新日時
    updated = models.DateTimeField(auto_now_add=True)
    
    #オブジェクトの文字列表現を定義（管理画面などでの表示に使用）
    def __str__(self):
        #タイトルを返す
        return self.title
    
    #モデルのメタ情報を定義
    class Meta:
        #作成日時の降順でソート（最新が最初）
        ordering = ['-created']
        
    
    @classmethod
    def get_comletion_stats(cls):
        
        #すべてのタスクを取得
        todos = cls.objects.all()
        
        #完了済みのタスクの数をカウント（completed=Trueのフィルターを適応）
        completed = todos.filter(completed=True).count()
        
        #未完了のタスクの数をカウント（completed=Falseのフィルターを適応）
        not_completed = todos.filter(completed=False).count()
        
        #総タスク数
        total = completed + not_completed
        
        #完了率を計算（パーセンテージで小数点以下2桁まで）
        #タスクが0件の場合は、ゼロ除算を避けて0を返す
        
        if total > 0:
            completion_rate = round((completed / total) * 100,2)
        else:
            completion_rate = 0
            
        return{
            'completed':completed,
            'not_completed':not_completed,
            'total':total,
            'completion_rate':completion_rate
        }
        
    @classmethod
    def get_todos_queryset(cls):
        
        #TodoデータをPandasのDataFrameに変換
        
        #すべてのタスクを取得（QuerySet）
        todos = cls.objects.all()
        
        
        #Django のQuerySetをPandasのDataFrameに変換
        #DataFrameはスプレッドシートのような表形式のデータ構造であり、
        #データ分析や菓子かを行う際に使用
        return todos
        
        
# Create your models here.
