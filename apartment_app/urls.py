from django.urls import path
from apartment_app.views import create_apartment_view, get_apartment_view, edit_apartment, apartment_view, delete_apartment

# Create your urls here.
# app_name = 'apartment_app'

urlpatterns = [
    path('create/', create_apartment_view, name="create_apartment"),
    path('flat/', get_apartment_view, name="get_apartment"),
    path('detail/<int:pk>/', apartment_view, name='detail'),
    path('update/<int:pk>/', edit_apartment, name='update_apartment'),
    path('delete/<int:pk>/', delete_apartment, name='delete_apartment'),
]