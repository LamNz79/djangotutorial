from django.db import transaction
from django.db.models import F

from polls.models import Choice


class ChoiceNotFound(Exception):
    pass


class InvalidVoteState(Exception):
    pass


def vote(choice_id: int) -> Choice:
    with transaction.atomic():
        updated = Choice.objects.filter(pk=choice_id).update(
            votes=F("votes") + 1
        )
    if updated == 0:
        raise ChoiceNotFound

    return Choice.objects.get(pk=choice_id)


def unvote(choice_id: int) -> Choice:
    with transaction.atomic():
        updated = Choice.objects.filter(
            pk=choice_id,
            votes__gt=0
        ).update(
            votes=F("votes") - 1
        )

    if updated == 0:
        if not Choice.objects.filter(pk=choice_id).exists():
            raise ChoiceNotFound
        raise InvalidVoteState

    return Choice.objects.get(pk=choice_id)
