from django.urls import path
from service_app.views import service_list_view

# Create your urls here.
# app_name = 'service_app'

urlpatterns = [
    path('list/', service_list_view, name="list"),
]