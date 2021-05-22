from rest_framework import serializers

from quests.models import TeamStatistic, Quest
from users.models import User


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_admin(
            username=validated_data['username'],
            password=validated_data['password']
        )


class TeamSerializer(serializers.ModelSerializer):
    quest = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile_name', 'quest']
        read_only_fields = ['username', 'quest']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_team(
            password=validated_data['password']
        )

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    class QuestTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Quest
            fields = ['id', 'title']
            read_only_fields = ['title']

    def get_quest(self, obj):
        try:
            return self.QuestTitleSerializer(TeamStatistic.objects.get(team=obj).quest).data
        except TeamStatistic.DoesNotExist:
            return None
