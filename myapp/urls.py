from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_excel, name="grafico"),
    path('export_template_excel/', views.export_template_excel, name='export_template_excel'),


]
