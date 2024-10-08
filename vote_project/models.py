from django.db import models
from grants_project.models import Project
from dateutil.relativedelta import relativedelta
from django.utils import timezone

class Vote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    total_yes = models.IntegerField(default=0) 
    total_no = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    start_date = models.DateTimeField('start date', default=timezone.now)
    end_date = models.DateTimeField('end date', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.project.name} votes'
    
class vote_history(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    validator_address = models.CharField(max_length=200)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    vote_result = models.IntegerField(default=0) # 0: no vote, 1: yes, 2: no
    vote_date = models.DateTimeField('vote date', auto_now_add=True)

    def __str__(self):
        return f'{self.project.name} vote history'

class Validator(models.Model):
    validator_address = models.CharField(max_length=200)
    reputation_score = models.IntegerField(default=0)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    def __str__(self):
        return self.validator_address