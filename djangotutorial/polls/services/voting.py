from django.db import transaction

from polls.models import Choice, Vote


class ChoiceNotFound(Exception):
    pass


class InvalidVoteState(Exception):
    pass


def vote(*, choice: Choice, user) -> Choice:
    """
       Cast a vote for a choice by a user.
       Single source of truth for vote creation.
       """
    with transaction.atomic():
        vote = Vote(
            user=user,
            choice=choice,
            question=choice.question,
        )
        vote.full_clean()
        vote.save()
        return choice


def unvote(*, choice: Choice, user) -> Choice:
    deleted, _ = Vote.objects.filter(
        user=user,
        choice=choice,
        question=choice.question,
    ).delete()
    if deleted == 0:
        raise InvalidVoteState
    return choice
