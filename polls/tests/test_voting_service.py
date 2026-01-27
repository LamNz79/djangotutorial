from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from polls.models import Question, Choice
from polls.services.voting import (
    vote,
    unvote,
    ChoiceNotFound,
    InvalidVoteState,
)
class VotingServiceTests(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            question_text="Best backend framework?",
            pub_date=timezone.now(),
        )

        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Django",
            votes=0,
        )

    def test_vote_requires_authentication(self):
        url = reverse("choices-vote", args=[self.choice.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_vote_increments_votes(self):
    #     updated_choice = vote(self.choice.id)
    #
    #     self.assertEqual(updated_choice.votes, 1)
    #
    #     self.choice.refresh_from_db()
    #     self.assertEqual(self.choice.votes, 1)
    #
    # def test_unvote_decrements_votes(self):
    #     vote(self.choice.id)
    #     vote(self.choice.id)
    #
    #     updated_choice = unvote(self.choice.id)
    #
    #     self.assertEqual(updated_choice.votes, 1)
    #
    # def test_unvote_at_zero_raises_error(self):
    #     with self.assertRaises(InvalidVoteState):
    #         unvote(self.choice.id)
    #
    #     self.choice.refresh_from_db()
    #     self.assertEqual(self.choice.votes, 0)
    #
    # def test_vote_nonexistent_choice_raises(self):
    #     with self.assertRaises(ChoiceNotFound):
    #         vote(9999)
