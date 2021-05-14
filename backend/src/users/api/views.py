from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from users.api.permissions import IsSuperuser
from users.api.serializerts import AdminSerializer, TeamSerializer
from users.models import User


class AdminListView(generics.ListCreateAPIView):
    permission_classes = (IsSuperuser, )
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    serializer_class = AdminSerializer


class TeamListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = User.objects.filter(is_staff=False)
    serializer_class = TeamSerializer


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = User.objects.filter(is_staff=False)
    serializer_class = TeamSerializer
