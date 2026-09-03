from django.urls import path
from contact_app.views import contact_view, contact_list_view, create_contact_view

# Create your urls here.
# app_name = 'contact_app'

urlpatterns = [
    path('detail/<int:pk>/', contact_view, name='detail'),
    path('create/', create_contact_view, name='create'),
    path('list/', contact_list_view, name='list'),
]