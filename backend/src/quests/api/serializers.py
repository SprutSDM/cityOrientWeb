from django.conf.global_settings import MEDIA_URL
from rest_framework import serializers

from quests.models import Quest, Task, Answer, TeamStatistic, TaskStatistic
from users.api.serializers import TeamSerializer


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
        print(quest_instance.preview)
        print(quest_instance.preview.url)
        return quest_instance

    def update(self, instance, validated_data):
        if 'tasks' in validated_data:
            tasks = validated_data.pop('tasks')
            instance.tasks.all().delete()
            self.recreate_tasks(instance, tasks=tasks)
        return super().update(instance, validated_data)


class QuestListSerializer(serializers.ModelSerializer):
    count_of_cp = serializers.SerializerMethodField()

    class Meta:
        model = Quest
        fields = ['id', 'title', 'place', 'count_of_cp', 'start_time', 'duration', 'preview']

    def get_count_of_cp(self, obj):
        return obj.tasks.count()

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


class QuestStatisticListSerializer(serializers.ModelSerializer):
    teams_statistic = TeamStatisticListSerializer(many=True)

    class Meta:
        model = Quest
        fields = ['teams_statistic']


class TaskStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatistic
        fields = ['id', 'tip_1_used', 'tip_2_used', 'lead_time']


class UseTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatistic
        fields = ['id', 'tip_1_used', 'tip_2_used', 'lead_time']
