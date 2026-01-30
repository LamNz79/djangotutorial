import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from polls.models import Vote


def test_user_cannot_vote_twice(db, user, choice):
    choice.vote(user)
    with pytest.raises(IntegrityError):
        choice.vote(user)


def test_vote_rejects_choice_from_different_question(db, user):
    from polls.models import Question, Choice

    q1 = Question.objects.create(
        question_text="Question 1?",
        pub_date="2025-01-01",
    )
    q2 = Question.objects.create(
        question_text="Question 2?",
        pub_date="2025-01-01",
    )

    choice = Choice.objects.create(
        question=q2,
        choice_text="Wrong choice",
    )

    vote = Vote(
        user=user,
        question=q1,  # question 1
        choice=choice,  # but choice from question 2
    )

    with pytest.raises(ValidationError):
        vote.full_clean()


def test_user_cannot_vote_twice_even_with_different_choices(db, user):
    from polls.models import Question, Choice

    q1 = Question.objects.create(
        question_text="Question 1?",
        pub_date="2025-01-01",
    )
    choice = Choice.objects.create(
        question=q1,
        choice_text="Wrong choice",
    )
    choice2 = Choice.objects.create(
        question=q1,
        choice_text="second choice",
    )

    choice.vote(user)
    with pytest.raises(IntegrityError):
        choice2.vote(user)


def test_both_user_vote_same_choice(db, user):
    from polls.models import Question, Choice

    q1 = Question.objects.create(
        question_text="Question 1?",
        pub_date="2025-01-01",
    )
    choice1 = Choice.objects.create(
        question=q1,
        choice_text="Wrong choice",
    )
    choice2 = Choice.objects.create(
        question=q1,
        choice_text="second choice",
    )

    user2 = User.objects.create_user(
        username="bob",
        password="secret123",
    )

    choice1.vote(user)
    choice2.vote(user2)
