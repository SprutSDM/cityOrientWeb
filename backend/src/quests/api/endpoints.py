from django.urls import path

from quests.api import views, viewsets

app_name = 'quests'
urlpatterns = [
    path('', views.QuestListView.as_view(), name='quests-list'),
    path('<int:pk>/', views.QuestDetailView.as_view(), name='quest-detail'),
    path('<int:pk>/statistic', views.QuestStatisticDetailView.as_view(), name="quest-statistic"),
    path('<int:pk>/join', viewsets.QuestViewSet.as_view({'post': 'join'}), name="quest-join"),
    path('<int:pk>/leave', views.QuestLeaveView.as_view(), name="quest-leave"),
    path('task/<int:pk>/complete', views.TaskCompleteView.as_view(), name="complete-task"),
    path('task/<int:pk>/use_tip/<int:tip_number>', views.UseTipView.as_view(), name="use-tip")
]
