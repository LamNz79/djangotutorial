from django.contrib import admin

from polls.models import Question, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ("Date information", {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "vote_count_display")
    list_select_related = ("question",)
    ordering = ("question",)

    def vote_count_display(self, obj):
        return obj.vote_set.count()

    vote_count_display.short_description = "Votes"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "choice", "created_at")
    readonly_fields = ("user", "question", "choice", "created_at")
