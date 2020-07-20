from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

from quests.models import TeamStatistic


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsQuestMember(BasePermission):
    def has_permission(self, request, view):
        team_statistic = TeamStatistic.objects.filter(quest=view.kwargs['pk'])
        if not team_statistic.exists():
            # Model doesn't exists, it's ok
            return True
        return team_statistic.first().team == request.user
