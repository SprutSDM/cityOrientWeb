from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api import views

app_name = 'users'
urlpatterns = [
    path('auth', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('admins', views.AdminListView.as_view(), name='quest-makers-list'),
    path('teams', views.TeamListView.as_view(), name='teams-list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail')
]
