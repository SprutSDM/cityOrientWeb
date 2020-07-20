from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quests.api.permissions import IsAdminOrReadOnly, IsQuestMember
from quests.api.serializers import QuestListSerializer, QuestDetailSerializer, \
    QuestStatisticListSerializer, QuestStatisticSerializer, QuestTaskSerializer
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


class QuestCompleteTaskView(generics.UpdateAPIView):
    permission_classes = (IsQuestMember,)
    serializer_class = QuestTaskSerializer

    def get_object(self):
        team_statistic = TeamStatistic.objects.filter(quest=self.kwargs['pk'], team=self.request.user).first()
        return TaskStatistic.objects.filter(task_id=self.kwargs['task_id'], team_statistic=team_statistic).first()
