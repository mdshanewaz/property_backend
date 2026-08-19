from django.urls import path
from rent_app.views import rent_list_view

# Create your urls here.
# app_name = 'rent_app'

urlpatterns = [
    path('rentlist/', rent_list_view, name='rent_list'),
]