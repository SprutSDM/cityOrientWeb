from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quests.api.permissions import IsAdminOrReadOnly
from quests.api.serializers import QuestListSerializer, QuestDetailSerializer, QuestStatisticListSerializer
from quests.models import Quest


class QuestListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Quest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestListSerializer
        return QuestDetailSerializer


class QuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Quest.objects.all()
    serializer_class = QuestDetailSerializer


class QuestStatisticDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Quest.objects.all()
    serializer_class = QuestStatisticListSerializer
