from django.urls import path
from . import views

urlpatterns = [
    path('test_connection/', views.test_connection, name='test_connection'),
    path('search/', views.search_view, name='search'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/<str:task_id>/', views.task_detail, name='task_detail'),
    path('', views.task_list, name='home'),  # Make task list the homepage
]