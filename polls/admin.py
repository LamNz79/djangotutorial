from dataclasses import field
from django.contrib import admin

from polls.models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,{'fields':['question_text']}),
        ("Date information",{'fields':['pub_date']})
    ]
    inlines=[ChoiceInline]
# Register your models here.
admin.site.register(Question,QuestionAdmin)