from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from quests.api.serializers import QuestDetailSerializer
from quests.models import Quest, Task, TeamStatistic, TaskStatistic


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestDetailSerializer

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        quest = self.get_object()

        tasks = Task.objects.filter(quest_id=quest.id)
        first_task = TeamStatistic.objects.filter(quest=quest.id).count() % tasks.count()
        team_statistic = TeamStatistic.objects.create(quest=quest, team=request.user, first_task=first_task)
        for task in tasks:
            TaskStatistic.objects.create(task=task, team_statistic=team_statistic)

        serializer = self.get_serializer(quest)
        return Response(serializer.data)
