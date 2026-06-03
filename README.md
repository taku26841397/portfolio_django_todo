# 📝 Todo 管理アプリ（Django）

自分のタスクを管理するために作成した Django 製の Todo アプリです。  
タイトル・メモ・完了状態・作成日・更新日を登録し、  
一覧・詳細・編集・削除ができる CRUD アプリケーションです。

ログイン機能を備え、認証済みユーザーのみが Todo を操作できるようにしています。  
また、matplotlib を使用したタスク統計ページも実装しています。

---

## 🌐 公開 URL
https://todo-1lnw.onrender.com/

---

## 🔑 テストユーザー
動作確認用のユーザーを用意しています。

- **ユーザー名：** testuser  
- **パスワード：** testpass123  

---

## 🛠 使用技術

### Backend
- Python 3.x  
- Django 5.x  
- Django Class-Based Views（ListView / DetailView / CreateView / UpdateView / DeleteView）  
- LoginRequiredMixin / SuccessMessageMixin  
- matplotlib（統計グラフ生成）  
- django-pandas（QuerySet → DataFrame 変換）  

### Frontend
- HTML / CSS  

### Infrastructure
- Render（デプロイ）  
- SQLite（開発環境）  

---

## 📌 機能一覧

### ✔ Todo 管理
- タスクの登録（タイトル / メモ / 完了状態）
- 一覧表示（ページネーション対応）
- 詳細表示
- 編集（UpdateView）
- 削除（DeleteView）

### ✔ 認証機能
- ログイン / ログアウト
- LoginRequiredMixin によるアクセス制御

### ✔ 統計ページ（Analytics）
- 完了 / 未完了の割合を円グラフで表示  
- 作成日の推移を棒グラフで表示  
- matplotlib で画像生成 → Base64 で HTML に埋め込み  

---

## 🎨 UI / デザインのポイント
- シンプルで見やすいレイアウト  
- Todo の完了状態を色分けして視認性を向上  
- CRUD 操作を直感的に行える UI  
- ログイン画面も統一感のあるデザインに調整  

---

## 🧩 工夫した点
- Django の **クラスベースビュー（CBV）** を活用し、コードの簡潔さと拡張性を重視  
- LoginRequiredMixin によるセキュリティ確保  
- matplotlib を使用し、サーバー側で統計グラフを生成   
- Render へのデプロイを通じて、本番環境での動作を確認  
- 本番 DB に **testuser** を作成し、企業がすぐに動作確認できるよう配慮  

---

## 📁 ディレクトリ構成（抜粋）

```
todoapp/            # Todo アプリのメイン機能
  ├── migrations/   # DB マイグレーション
  ├── templates/    # HTML テンプレート
  ├── static/       # CSS
  ├── models.py     # Todo モデル
  ├── views.py      # CRUD + Analytics
  ├── urls.py       # アプリ内 URL
  └── forms.py

webapp/             # Django プロジェクト設定
  ├── settings.py
  ├── urls.py
  └── wsgi.py

manage.py           # Django の起動スクリプト
requirements.txt    # 使用パッケージ一覧
```

---

## 📄 ライセンス
このプロジェクトは学習目的で作成したものです。
