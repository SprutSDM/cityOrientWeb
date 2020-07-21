from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

from quests.models import TeamStatistic


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsQuestMember(BasePermission):
    def has_permission(self, request, view):
        team_statistic = TeamStatistic.objects.filter(quest=view.kwargs['pk'], team=request.user)
        return team_statistic.exists()
