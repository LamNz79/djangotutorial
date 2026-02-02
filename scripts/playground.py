# scripts/playground.py
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # adjust
django.setup()

from polls.models import Question
from django.db.models import Count

qs = (
    Question.objects
    .annotate(total_votes=Count("vote"))
    .prefetch_related("choice_set")
)

for q in qs:
    print(q.question_text)
    for c in q.choice_set.all():
        print("  -", c.choice_text)
