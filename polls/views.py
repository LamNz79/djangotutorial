from django.db.models.aggregates import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from polls.models import Choice, Question
from polls.permissions import IsStaffUser
from polls.serializers import QuestionSerializers, ChoiceSerializer
from polls.services.voting import vote, ChoiceNotFound, unvote, InvalidVoteState


class ChoiceViewSet(viewsets.ModelViewSet):
    """
      Contract-driven ViewSet for Choice voting actions.
      No CRUD exposure.
    """

    def get_object(self) -> Choice:
        return get_object_or_404(Choice, pk=self.kwargs["pk"])

    def get_permissions(self):
        if self.action == "vote":
            return [IsAuthenticated()]
        elif self.action == "unvote":
            permission_classes = [IsStaffUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["POST"])
    def vote(self, request, pk: int) -> Response:
        try:
            choice = vote(pk)
        except ChoiceNotFound:
            return Response(
                {"error": "choice_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ChoiceSerializer(choice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def un_vote(self, request, pk: int) -> Response:
        try:
            choice = unvote(pk)
        except ChoiceNotFound:
            return Response(
                {"error": "choice_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvalidVoteState:
            return Response(
                {"error": "invalid_vote_state"},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = ChoiceSerializer(choice)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionList(viewsets.ModelViewSet):
    """
        Contract-driven ViewSet for Questions.
        Exposes list + retrieve only.
    """
    serializer_class = QuestionSerializers
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Question.objects
            .annotate(total_votes=Sum("choice__votes"))
            .prefetch_related("choice_set")
        )
