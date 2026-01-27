from django.urls import path
from rest_framework.routers import DefaultRouter

from polls import views

from .views import QuestionList,  ChoiceViewSet

router = DefaultRouter()
router.register(r"choices", ChoiceViewSet, basename="choices")
router.register(r"questions", QuestionList,basename="questions")
urlpatterns = router.urls

# urlpatterns = [
#     path("questions/", QuestionList.as_view(), name="question-list"),
#
# ]
