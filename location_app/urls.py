from django.urls import path
from location_app.views import division_view, district_view

# Create your urls here.
# app_name = 'location_app'

urlpatterns = [
    path('division/', division_view, name="division"),
    path('district/<int:pk>', district_view, name="district"),
]