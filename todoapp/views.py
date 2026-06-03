from django.shortcuts import render
from  . import models
from .forms import TodoForm

from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.contrib.messages.views import SuccessMessageMixin

import io #画像を一時的にメモリに保存するために使用
import base64 #画像データを文字列（テキスト）に変換するために使用
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt  #グラフ等がライブラリ
from django.shortcuts import render
from django.views import View

#ログイン状態をチェック
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

#ログイン状態・権限状態をチェックするためにインポート


from .models import Todo

def get_todos_dataframe():
    
    from django_pandas.io import read_frame
    
    qs = Todo.get_todos_queryset()
    df = read_frame(qs)
    return df


    

class TodoListView(LoginRequiredMixin,ListView):
    #使用するモデルを指定（Todoモデル ）
    model = models.Todo
    #使用するテンプレートファイルを指定
    template = 'todoapp/todo_list.html'
    #テンプレートで使用するオブジェクトリストの名前を指定
    context_object_name = 'todos'
    
    paginate_by = 2
    


class TodoDetailView(LoginRequiredMixin,DetailView):
    model = models.Todo
    
    template_name = 'todoapp/todo_detail.html'
    
    context_object_name = 'todo'


class TodoCreateView(SuccessMessageMixin,LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.Todo
    
    template_name = 'todoapp/todo_create.html'
    
    form_class = TodoForm
    
    #登録成功時のリダイレクト先を指定
    success_url = reverse_lazy('todo_list')
    
    #登録成功時のメッセージを追加
    success_message = 'Todoが「登録」されました。'
    
    #作成権限追加
    # permission_required = 'todoapp.add_todo'

class TodoUpdateView(SuccessMessageMixin,LoginRequiredMixin,PermissionRequiredMixin,UpdateView):

    model = models.Todo
    
    template_name = 'todoapp/todo_update.html'

    #TodoFormを使用するように変更
    form_class = TodoForm
    
    success_url = reverse_lazy('todo_list')
    
    #成功メッセージの追加
    success_message = 'Todoが「更新」されました。'
    
    # permission_required = 'todoapp.change_todo'
    
    #フォームのバリデーション（入力チェック）が成功した後に呼ばれるメソッド
    def form_valid(self,form):
        
        #フォームのデータを保存し、Todoインスタンスを取得
        todo = form.save()
        #ターミナルに更新情報を記録（タイトルと交信取得）
        print(f"タイトル：'{todo.title}' 更新時間：'{localtime(todo.updated)}'")
        #親クラスのform_validを実行し、処理を続行
        return super().form_valid(form)
        
        
class TodoDeleteView(SuccessMessageMixin,LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.Todo
    
    template_name = 'todoapp/todo_confirm_delete.html'
    
    context_object_name = 'todo'
    
    success_url = reverse_lazy('todo_list')
    
    #成功メッセージの追加
    success_message = 'Todoが「削除」されました。'
    
    # permission_required = 'todoapp.delete_todo'
    
class TodoAnalyticsView(LoginRequiredMixin,View):
    template_name = 'todoapp/todo_analytics.html'
    
    #GETリクエスト（ページの表示）が来たときに実行されるメソッド
    def get(self,request,*args,**kwargs):
        
        #Todoモデルから完了・未完了の統計データを取得
        stats = models.Todo.get_comletion_stats()
        
        #グラフの枠組みを作成(1行2列、サイズは横12×5インチ)
        fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,5))


        #-----左側：円グラフ-----
        
        #グラフのラベルを設定
        labels = ['Completed','Incompled'] #完了と未完了
        #グラフの値（完了タスク数と未完了タスク数）
        sizes = [stats['completed'],stats['not_completed']]
        #グラフの色設定（完了は緑、未完了はピンク）
        colors = ['#66FF99','#FF3399']
        
        #円グラフを描画
        #autopct='%1.1f%%'：各部分に割合を表示
        #startangle=90：円グラフの開始角度を90度に設定
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle = 90)
        
        #円グラフを真円に保つ設定
        ax1.axis('equal')
        
        #グラフのタイトル設定
        ax1.set_title('Task Completion')
        
        
        
        #-----右側：棒グラフ-----
        #Todo　モデルからデータをDataFrame形式で取得
        df = get_todos_dataframe()
        
        #データが存在する場合のみグラフを作成
        if not df.empty:
            #作成日の日付部分だけを取り出して新しい列を作成
            #df['created']にはDateTime型のデータがはいっているので、
            #.dt.date　で日付部分だけ取り出す
            df['created_date'] = df['created'].dt.date
            
            #作成日ごとにタスク数をカウント
            #groupby('created_date')：作成日でグループ化
            #size()：各グループのタスク数をカウント
            daily_counts = df.groupby('created_date').size()
            
            #最新の7件のみを取得
            resent_counts = daily_counts.tail(7)
            
            #　Y軸の最大値を5に設定
            ax2.set_ylim(0,5)
            
            #棒グラフを描画
            resent_counts.plot(kind = 'bar', ax=ax2, color='#4e73dF')
            
            #X軸のラベルを回転させて重なりを防ぐ
            plt.xticks(rotation=20)
            
            #タイトルと軸ラベルを英語で設定
            ax2.set_title('Recent Task Creation')
            ax2.set_ylabel('Number of Tasks')
            ax2.set_xlabel('Creation Date')
            
            
            
            #----グラフをイメージデータに変換-----

            #メモリ上に一時的なバッファを作成
            buffer = io.BytesIO()
            #グラフのレイアウトを調整(グラフ同士が重ならないように)
            plt.tight_layout()
            #グラフをPNG形式で一時バッファに保存
            plt.savefig(buffer,format='png')
            #バッファの読み取り位置を先頭に戻す
            buffer.seek(0)
            #バッファからイメージデータを取得
            image_png = buffer.getvalue()
            #バッファを閉じる
            buffer.close()
            
            
            
            #イメージデータをBase64に形式に変換（テキスト形式）に変換
            #これによりHTMLに直接埋め込めるようになる
            graph = base64.b64encode(image_png).decode('utf-8')
            
            
            context = {
                'stats':stats,  #統計データ
                'graph':graph,  #グラフのBase64エンコードされたデータ
            }
            
            
            return render(request,self.template_name,context)
            

# Create your views here.
