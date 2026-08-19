from django.urls import path
from land_app.views import create_land_view, lands_list_view, land_view, land_update_view, land_delete_view

# Create your urls here.
# app_name = 'land_app'

urlpatterns = [
    path("create/", create_land_view, name="register"),
    path("landlist/", lands_list_view, name="land_list"),
    path("detail/<int:pk>/", land_view, name="land_detail"),
    path("update/<int:pk>/", land_update_view, name="land_update"),
    path("delete/<int:pk>/", land_delete_view, name="land_delete"),
]