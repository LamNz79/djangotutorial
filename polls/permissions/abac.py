from django.utils import timezone
from rest_framework.permissions import BasePermission


class CanVote(BasePermission):
    def has_object_permission(self, request, view, obj):
        question = obj.question
        return question.pub_date <= timezone.now()
