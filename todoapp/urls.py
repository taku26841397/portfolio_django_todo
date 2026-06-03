from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.TodoListView.as_view(),name='todo_list'),
    path('<int:pk>/',views.TodoDetailView.as_view(),name='todo_detail'),
    path('new/',views.TodoCreateView.as_view(),name='todo_create'),
    path('<int:pk>/edit/',views.TodoUpdateView.as_view(),name='todo_update'),
    path('<int:pk>/delete/',views.TodoDeleteView.as_view(),name='todo_delete'),
    path('analytics/',views.TodoAnalyticsView.as_view(),name='todo_analytics'),
    
]
