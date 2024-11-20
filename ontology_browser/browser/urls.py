from django.urls import path
from . import views

urlpatterns = [
    path('test_connection/', views.test_connection, name='test_connection'),
    path('search/', views.search_view, name='search'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/<str:task_id>/', views.task_detail, name='task_detail'),
    path('concepts/', views.concept_list, name='concept_list'),
    path('concepts/search/', views.concept_search, name='concept_search'),
    path('concept/<str:concept_id>/', views.concept_detail, name='concept_detail'),
    path('', views.home, name='home'),
]