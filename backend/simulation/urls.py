from django.urls import path
from . import views

urlpatterns = [
    path('run/', views.run_simulation, name='run_simulation'),
    path('export/<int:simulation_id>/', views.export_simulation_pdf, name='export_simulation_pdf'),
]