from datetime import datetime, timedelta

import pytz
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quests.api.serializers import QuestDetailSerializer, TaskStatisticSerializer
from quests.models import Quest, Task, TeamStatistic, TaskStatistic


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestDetailSerializer
    permission_classes = (IsAuthenticated, )

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

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        quest = self.get_object()
        quest.teams_statistic.filter(team=self.request.user).delete()
        serializer = self.get_serializer(quest)
        return Response(serializer.data)


class TaskStatisticViewSet(viewsets.ModelViewSet):
    queryset = TaskStatistic.objects.all()

    serializer_class = TaskStatisticSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = Task.objects.get(id=pk)
        team_statistic = TeamStatistic.objects.get(team=request.user)
        task_statistic = team_statistic.tasks_statistic.get(task=task)
        date = datetime.now(tz=pytz.utc) + timedelta(hours=3) - task_statistic.team_statistic.quest.start_time
        task_statistic.lead_time = (datetime.min + date).time()
        task_statistic.save()
        serializer = self.get_serializer(task_statistic)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def use_tip(self, request, pk=None, tip_number=None):
        task = Task.objects.get(id=pk)
        team_statistic = TeamStatistic.objects.get(team=request.user)
        task_statistic = team_statistic.tasks_statistic.get(task=task)
        if tip_number == 0:
            task_statistic.tip_1_used = True
        elif tip_number == 1:
            task_statistic.tip_2_used = True
        else:
            raise ValidationError(detail="Given invalid tip number")
        task_statistic.save()
        serializer = self.get_serializer(task_statistic)
        return Response(serializer.data)
