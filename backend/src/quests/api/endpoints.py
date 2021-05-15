from django.urls import path

from quests.api import views, viewsets

app_name = 'quests'
urlpatterns = [
    path('', views.QuestListView.as_view(), name='quests-list'),
    path('<int:pk>/', views.QuestDetailView.as_view(), name='quest-detail'),
    path('<int:pk>/statistic', views.QuestStatisticDetailView.as_view(), name="quest-statistic"),
    path('<int:pk>/join', viewsets.QuestViewSet.as_view({'post': 'join'}), name="quest-join"),
    path('<int:pk>/leave', viewsets.QuestViewSet.as_view({'post': 'leave'}), name="quest-leave"),
    path('task/<int:pk>/complete', viewsets.TaskStatisticViewSet.as_view({'post': 'complete'}), name="complete-task"),
    path('task/<int:pk>/use_tip/<int:tip_number>', viewsets.TaskStatisticViewSet.as_view({'post': 'use_tip'}), name="use-tip")
]
