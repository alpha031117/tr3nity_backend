from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Grant(models.Model):
    organisation = models.CharField(max_length=255, help_text="Name of the grants organization")
    program_name = models.CharField(max_length=255, help_text="Name of the grant program")
    description = models.TextField(help_text="Detailed description of the grant program")
    start_fund = models.DateTimeField(help_text="Start date and time for the funding period")
    end_fund = models.DateTimeField(help_text="End date and time for the funding period")
    matching_pool = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        help_text="Total amount in the matching pool"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_fund']

    def __str__(self):
        return f"{self.program_name} by {self.organisation}"

    def is_active(self):
        now = timezone.now()
        return self.start_fund <= now <= self.end_fund

    def days_remaining(self):
        if self.end_fund > timezone.now():
            return (self.end_fund - timezone.now()).days
        return 0

class Project(models.Model):
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='ogranisation')
    name = models.CharField(max_length=255, help_text="Name of the project")
    description = models.TextField(help_text="Detailed description of the project")
    start_time = models.DateTimeField(help_text="Start date and time of the project")
    end_time = models.DateTimeField(help_text="End date and time of the project")
    current_fund = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Current amount of funding received"
    )
    total_contributors = models.PositiveIntegerField(
        default=0,
        help_text="Total number of contributors to the project"
    )
    team_members = models.TextField(help_text="List of team members, comma-separated")
    pdf_uploaded = models.CharField(max_length=255, help_text="PDF uploaded file", blank=True, default='')
    aim = models.TextField(help_text="Aim of the project", blank=True, default='')
    timeline = models.TextField(help_text="Timeline of the project", blank=True, default='')
    created_by = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='active')

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.name}"

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def funding_progress(self):
        if self.needed_fund > 0:
            return (self.current_fund / self.needed_fund) * 100
        return 0

    def days_remaining(self):
        if self.end_time > timezone.now():
            return (self.end_time - timezone.now()).days
        return 0

    def get_team_members_list(self):
        return [member.strip() for member in self.team_members.split(',') if member.strip()]