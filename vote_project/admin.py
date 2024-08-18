from django.contrib import admin
from .models import Vote, Validator, vote_history

# Register your models here.
admin.site.register(Vote)
admin.site.register(Validator)
admin.site.register(vote_history)
