from django.utils import timezone
from rest_framework.permissions import BasePermission

from polls.models import Vote, Choice


class CanVote(BasePermission):
    def has_object_permission(self, request, view, obj: Choice):
        choice = obj
        question = choice.question
        if question.pub_date > timezone.now():
            return False

        return not Vote.objects.filter(
            user=request.user,
            choice=choice,
            question=choice.question
        ).exists()
