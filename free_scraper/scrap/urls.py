from django.urls import path
from scrap import views

urlpatterns = [
    path('', views.home),
    path('candidates', views.export_candidates),
    path('projects', views.export_projects),
    path('bids', views.export_bids)
]