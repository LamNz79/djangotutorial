from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from polls.domain.voting.errors import VotingError
from polls.models import Choice, Question
from polls.permissions.abac import CanVote
from polls.permissions.permissions import IsVoter, IsModerator
from polls.security.actions import Actions
from polls.security.audit import log_audit_event
from polls.security.policy.voting import can_vote
from polls.serializers import QuestionSerializers, ChoiceSerializer, QuestionCreateSerializer, ChoiceCreateSerializer
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
        )

    def get_permissions(self):
        if self.action == "vote":
            return [IsVoter(), CanVote()]
        elif self.action == "un_vote":
            return [IsModerator()]
        return super().get_permissions()

    @action(detail=False, methods=["POST"])
    def vote(self, request, pk=None):
        choice_id = request.data.get("choiceId")

        if not choice_id:
            return Response(
                {"error": "choice_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        choice = get_object_or_404(
            Choice.objects
            .annotate(vote_count=Count("vote")),
            pk=choice_id,
        )

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

    @action(detail=False, methods=["POST"])
    def un_vote(self, request) -> Response:
        try:
            choice_id = request.data.get("choiceId")

            if not choice_id:
                return Response(
                    {"error": "choice_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            choice = get_object_or_404(
                Choice.objects
                .annotate(vote_count=Count("vote")),
                pk=choice_id,
            )

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

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return []
        elif self.action == "create":
            return [IsModerator()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("create", "create_list"):
            return QuestionCreateSerializer
        return QuestionSerializers

    @action(
        detail=False,
        methods=["POST"],
        url_path="create-list"

    )
    def create_list(self, request):
        serializer = self.get_serializer(
            data=request.data,
            many=True,
        )
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        return Response(
            QuestionSerializers(question, many=True).data,
            status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["POST"],
        url_path="add-choice"
    )
    def add_choice(self, request, pk=None):
        question = self.get_object()
        serializer = ChoiceCreateSerializer(
            data=request.data,
            many=True,

        )
        serializer.is_valid(raise_exception=True)
        choices = [
            Choice(question=question, **item)
            for item in serializer.validated_data
        ]
        Choice.objects.bulk_create(choices)
        return Response(
            ChoiceSerializer(
                Choice.objects.filter(question=question),
                many=True
            ).data,
            status.HTTP_201_CREATED
        )

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
