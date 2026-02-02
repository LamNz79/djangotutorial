import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from polls.models import Question, Choice

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="secret123",
    )


@pytest.fixture
def choice(db):
    question = Question.objects.create(
        question_text="Test question?",
        pub_date=timezone.now(),
    )
    return Choice.objects.create(
        question=question,
        choice_text="Yes",
    )
