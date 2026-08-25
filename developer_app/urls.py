from django.urls import path
from developer_app.views import developer_list_view, developer_create_view, developer_delete_view, developer_update_view, developer_view

# Create your urls here.
# app_name = 'rent_app'

urlpatterns = [
    path('create/', developer_create_view, name='developer_create'),
    path('detail/<int:pk>/', developer_view, name='developer_detail'),
    path('developerlist/', developer_list_view, name='developer_list'),
    path('update/<int:pk>/', developer_update_view, name='developer_update'),
    path('delete/<int:pk>/', developer_delete_view, name='developer_delete'),
]