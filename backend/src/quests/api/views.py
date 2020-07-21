from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from quests.api.permissions import IsAdminOrReadOnly, IsQuestMember
from quests.api.serializers import QuestListSerializer, QuestDetailSerializer, \
    QuestStatisticListSerializer, QuestStatisticSerializer, TaskStatisticSerializer, UseTipSerializer
from quests.models import Quest, TeamStatistic, TaskStatistic


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


class QuestJoinView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Quest.objects.all()
    serializer_class = QuestStatisticSerializer

    def perform_create(self, serializer):
        serializer.save(team=self.request.user, quest_id=self.kwargs['pk'])


class TaskCompleteView(generics.UpdateAPIView):
    permission_classes = (IsQuestMember,)
    serializer_class = TaskStatisticSerializer

    def get_object(self):
        return get_object_or_404(TaskStatistic.objects.all(), task=self.kwargs['pk'])


class UseTipView(generics.UpdateAPIView):
    permission_classes = (IsQuestMember,)
    serializer_class = UseTipSerializer

    def get_object(self):
        return get_object_or_404(TaskStatistic.objects.all(), task=self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save(tip_number=self.kwargs['tip_number'])
