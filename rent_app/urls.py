from django.urls import path
from rent_app.views import rent_list_view, rent_create_view, rent_delete_view, rent_update_view, rent_view

# Create your urls here.
# app_name = 'rent_app'

urlpatterns = [
    path('create/', rent_create_view, name='rent_create'),
    path('detail/<int:pk>/', rent_view, name='rent_detail'),
    path('rentlist/', rent_list_view, name='rent_list'),
    path('update/<int:pk>/', rent_update_view, name='rent_update'),
    path('delete/<int:pk>/', rent_delete_view, name='rent_delete'),
]