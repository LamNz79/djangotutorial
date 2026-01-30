from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

    def vote(self, user):
        """
        Cast a vote for this choice by a user.
        Enforces one-vote-per-user-per-choice.
        """
        vote = Vote.objects.create(user=user, question=self.question, choice=self)
        try:
            vote.full_clean()
            vote.save()
            return True
        except IntegrityError:
            return False

    @property
    def vote_count(self):
        return self.votes.count()


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="unique_vote_per_question"
            )
        ]

    def clean(self):
        if self.choice.question.pk != self.question.pk:
            raise ValidationError("Choice does not belong to the given question")
