from django.urls import path, include

urlpatterns = [
    path('api/quests/', include('quests.api.endpoints')),
    path('api/users/', include('users.api.endpoints'))
]
