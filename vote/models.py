from django.db import models

# Create your models here.

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_description = models.CharField(max_length=200)
    funded_amount = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user_address = models.CharField(max_length=200)

    def __str__(self):
        return self.project_name
    
class Vote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    total_yes = models.IntegerField(default=0) 
    total_no = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.project.project_name} votes'
    
class vote_history(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    validator_address = models.CharField(max_length=200)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    vote_result = models.IntegerField(default=0) # 0: no vote, 1: yes, 2: no
    vote_date = models.DateTimeField('vote date', auto_now_add=True)

    def __str__(self):
        return f'{self.project.project_name} vote history'

class Validator(models.Model):
    validator_address = models.CharField(max_length=200)
    reputation_score = models.IntegerField(default=0)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    def __str__(self):
        return self.validator_address