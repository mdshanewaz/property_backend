from django.urls import path
from land_app.views import create_land_view

# Create your urls here.
# app_name = 'land_app'

urlpatterns = [
    path("create/", create_land_view, name="register"),
]