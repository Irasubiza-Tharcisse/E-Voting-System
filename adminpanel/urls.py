from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='admin_dashboard'),
    path('elections/', manage_elections, name='admin_elections'),
    path('positions/', manage_positions, name='admin_positions'),
    path('candidates/', manage_candidates, name='admin_candidates'),
    path('manage-admins/',manage_admins, name='manage_admins'),
    path('approve-admin/<int:user_id>/', approve_admin, name='approve_admin'),
    path('deny-admin/<int:user_id>/', deny_admin, name='deny_admin'),
]
