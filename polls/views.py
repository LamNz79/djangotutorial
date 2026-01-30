from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from polls.domain.voting.errors import VotingError
from polls.models import Choice, Question
from polls.permissions.abac import CanVote
from polls.permissions.permissions import IsVoter, IsModerator
from polls.security.actions import Actions
from polls.security.audit import log_audit_event
from polls.security.policy.voting import can_vote
from polls.serializers import QuestionSerializers, ChoiceSerializer
from polls.services.voting import vote, ChoiceNotFound, unvote, InvalidVoteState


class ChoiceViewSet(viewsets.ModelViewSet):
    """
      Contract-driven ViewSet for Choice voting actions.
      No CRUD exposure.
    """

    def get_object(self) -> Choice:
        return get_object_or_404(
            Choice.objects.
            annotate(vote_count=Count("vote"))
            .order_by('-vote_count'),
            pk=self.kwargs["pk"])

    def get_permissions(self):
        if self.action == "vote":
            return [IsVoter(), CanVote()]
        elif self.action == "unvote":
            return [IsModerator()]
        return super().get_permissions()

    @action(detail=True, methods=["POST"])
    def vote(self, request, pk=None):
        choice = self.get_object()

        decision = can_vote(
            request=request,
            view=self,
            choice=choice,
        )
        log_audit_event(
            user_id=request.user.id,
            action=Actions.VOTE,
            resource=f"choice: {choice.pk} - {choice.choice_text}",
            allowed=decision.allowed,
            reason=decision.reason,
        )
        if not decision.allowed:
            return Response(
                {"error": decision.reason},
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ Business logic (unchanged)
        res = vote(choice=choice, user=request.user)
        serializer = ChoiceSerializer(res)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def un_vote(self, request, pk: int) -> Response:
        try:
            choice = self.get_object()
            res = unvote(choice=choice, user=request.user)
        except ChoiceNotFound:
            return Response(
                {"error": VotingError.CHOICE_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvalidVoteState:
            return Response(
                {"error": VotingError.INVALID_VOTE_STATE},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = ChoiceSerializer(res)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    """
        Contract-driven ViewSet for Questions.
        Exposes list + retrieve only.
    """
    serializer_class = QuestionSerializers
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Question.objects
            .annotate(total_votes=Count("vote"))
            .prefetch_related(
                Prefetch(
                    "choice_set",
                    queryset=Choice.objects.annotate(
                        vote_count=Count("vote"))
                )
            )
            .order_by("-total_votes")

        )
