from datetime import datetime, timedelta
import pytz

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from quests.models import Quest, Task, Answer, TeamStatistic, TaskStatistic
from users.api.serializerts import TeamSerializer


class TaskDetailSerializer(serializers.ModelSerializer):
    answers = serializers.ListSerializer(required=True, child=serializers.CharField())

    class Meta:
        model = Task
        fields = ['id', 'answers', 'content', 'tip_1', 'tip_2', 'title']


class QuestDetailSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(many=True, required=True)

    class Meta:
        model = Quest
        fields = '__all__'

    def recreate_tasks(self, instance, tasks):
        for task in tasks:
            answers = task.pop('answers')
            task_instance = Task.objects.create(quest=instance, **task)
            for answer in answers:
                Answer.objects.create(task=task_instance, answer=answer)

    def create(self, validated_data):
        tasks = validated_data.pop('tasks')
        quest_instance = Quest.objects.create(**validated_data)
        self.recreate_tasks(quest_instance, tasks=tasks)
        return quest_instance

    def update(self, instance, validated_data):
        tasks = validated_data.pop('tasks')
        instance.tasks.all().delete()
        self.recreate_tasks(instance, tasks=tasks)
        return super().update(instance, validated_data)


class QuestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['id', 'title', 'place', 'start_time', 'duration']


class TaskStatisticListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatistic
        fields = ['id', 'task', 'tip_1_used', 'tip_2_used', 'lead_time']


class TeamStatisticListSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    tasks_statistic = TaskStatisticListSerializer(many=True)

    class Meta:
        model = TeamStatistic
        fields = ['id', 'team', 'tasks_statistic']
        read_only_fields = ['id', 'team', 'tasks_statistic']


class QuestStatisticSerializer(serializers.ModelSerializer):
    tasks_statistic = TaskStatisticListSerializer(many=True, required=False)

    class Meta:
        model = TeamStatistic
        fields = ['id', 'team', 'quest', 'tasks_statistic', 'first_task']
        read_only_fields = ['id', 'team', 'quest', 'tasks_statistic', 'first_task']

    def create(self, validated_data):
        tasks = Task.objects.filter(quest_id=validated_data['quest_id'])
        first_task = TeamStatistic.objects.filter(quest=validated_data['quest_id']).count() % tasks.count()
        team_statistic = TeamStatistic.objects.create(**validated_data, first_task=first_task)
        for task in tasks:
            TaskStatistic.objects.create(task=task, team_statistic=team_statistic)
        return team_statistic


class QuestStatisticListSerializer(serializers.ModelSerializer):
    teams_statistic = TeamStatisticListSerializer(many=True)

    class Meta:
        model = Quest
        fields = ['teams_statistic']


class TaskStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatistic
        fields = ['id', 'tip_1_used', 'tip_2_used', 'lead_time']

    def update(self, instance, validated_data):
        date = datetime.now(tz=pytz.utc) + timedelta(hours=3) - instance.team_statistic.quest.start_time
        instance.lead_time = (datetime.min + date).time()
        instance.save()
        return instance


class UseTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatistic
        fields = ['id', 'tip_1_used', 'tip_2_used', 'lead_time']

    def update(self, instance, validated_data):
        tip_number = validated_data["tip_number"]
        if tip_number == 0:
            instance.tip_1_used = True
        elif tip_number == 1:
            instance.tip_2_used = True
        else:
            raise ValidationError(detail="Given invalid tip number")
        instance.save()
        return instance
