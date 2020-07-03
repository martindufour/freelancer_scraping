from django.db import models

# Create your models here.
class MCandidate(models.Model):
    name = models.CharField(max_length=100)
    nstars = models.FloatField()
    nreviews = models.IntegerField()
    jobs_completed = models.FloatField(blank=True, null=True)
    on_budget = models.FloatField(blank=True, null=True)
    on_time = models.FloatField(blank=True, null=True)
    repeat_hire_rate = models.FloatField(blank=True, null=True)
    description = models.TextField()
    visited = models.BooleanField(default=False)

class MProject (models.Model):
    url = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    visited = models.BooleanField(default=False)

class MBids (models.Model):
    bider = models.ForeignKey(MCandidate, on_delete=models.CASCADE)
    project = models.ForeignKey(MProject, on_delete=models.CASCADE)
    description = models.TextField(default=None)
    price = models.FloatField(default=None)
    currency = models.CharField(default=None, max_length=7)
    ndays = models.IntegerField(default=None, blank=True, null=True)
    status = models.BooleanField()