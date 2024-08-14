from django.contrib import admin
from .models import Project, Vote, Validator, vote_history

# Register your models here.
admin.site.register(Project)
admin.site.register(Vote)
admin.site.register(Validator)
admin.site.register(vote_history)
