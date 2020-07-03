from django.shortcuts import render
from django.http import HttpResponse
import csv
from .models import MCandidate
from .models import MProject
from .models import MBids
# Create your views here.

def home(request):
    return HttpResponse(
        """
        <p> <a href='/candidates'> Candidates </a> </p>
        <p> <a href='/projects'> Projects </a> </p>
        <p> <a href='/bids'> Bids </a> </p>
        """
    )

def export_candidates(request):
    response = HttpResponse(content_type='text/csv')

    fieldnames = [
        'id',
        'name',
        'nstars',
        'nreviews',
        'jobs_completed',
        'on_budget',
        'on_time',
        'repeat_hire_rate',
        'description'
    ]
    #[f.name for f in MCandidate._meta.get_fields()]
    writer = csv.writer(response)
    writer.writerow(fieldnames)

    candidates_list = list(MCandidate.objects.values_list(
        'pk',
        'name',
        'nstars',
        'nreviews',
        'jobs_completed',
        'on_budget',
        'on_time',
        'repeat_hire_rate',
        'description'
    ))

    for c in candidates_list:
        writer.writerow(c)

    response['Content-Disposition'] = 'attachment; filename="candidates.csv'
    return response

def export_bids(request):
    response = HttpResponse(content_type='text/csv')

    fieldnames = [
        'bider',
        'project',
        'description',
        'price',
        'currency',
        'ndays',
        'status'
    ]

    writer = csv.writer(response)
    writer.writerow(fieldnames)

    bids_list = list(MBids.objects.values_list(
        'bider',
        'project',
        'description',
        'price',
        'currency',
        'ndays',
        'status'
    ))

    for c in bids_list:
        writer.writerow(c)

    response['Content-Disposition'] = 'attachment; filename="bids.csv'
    return response

def export_projects(request):
    response = HttpResponse(content_type='text/csv')

    fieldnames = [
        'id',
        'url',
        'description',
        'skills',
    ]

    writer = csv.writer(response)
    writer.writerow(fieldnames)

    projects_list = list(MProject.objects.exclude(description='').values_list(
        'pk',
        'url',
        'description',
        'skills',
    ))

    for c in projects_list:
        writer.writerow(c)

    response['Content-Disposition'] = 'attachment; filename="projects.csv'
    return response