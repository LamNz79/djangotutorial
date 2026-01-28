from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import timezone

from polls.models import Choice, Question

User = get_user_model()


class ChoiceAuthAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            password="secret123"
        )

        self.choice = Choice.objects.create(
            question=Question.objects.create(
                question_text="Test?",
                pub_date=timezone.datetime.now()
            ),
            choice_text="Yes",
            votes=0
        )

    def test_vote_requires_authentication(self):
        url = reverse("choice-vote", args=[self.choice.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vote_with_token_succeeds(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("choice-vote", args=[self.choice.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
