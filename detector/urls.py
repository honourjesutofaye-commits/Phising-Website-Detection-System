from django.urls import path
from . import views

app_name = "detector"

urlpatterns = [
    path("", views.landing, name="landing"),
    # Keep the original route name so existing template links continue to work.
    path("analyze/", views.index, name="index"),
]
