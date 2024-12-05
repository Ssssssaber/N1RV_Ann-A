from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('services/<int:service_id>/edit/', views.service_edit_view, name='edit_service'),
    path('services/create/', views.service_create_view, name='create_service'),
    path('services/<int:service_id>/delete/', views.service_delete_view,
         name='delete_service'),
    
    path('hairdresser/list', views.hairdresser_list,
         name='hairdresser_list'),
    path('hairdresser/create', views.hairdresser_create_view,
         name='create_hairdresser'),
    path('hairdresser/<slug:hairdresser_slug>/edit', views.hairdresser_edit_view,
         name='edit_hairdresser'),
    path('hairdresser/<slug:hairdresser_slug>/delete', views.hairdresser_delete_view,
         name='delete_hairdresser'),
    path('hairdresser/<slug:hairdresser_slug>', views.hairdresser_services,
         name='hairdresser_services'),

    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('services/<int:service_id>/order/', views.order_create_view,
         name='create_order'),
    path('services/<int:service_id>/edit_order/<int:order_id>/',
         views.order_edit_view, name='edit_order'),
    path('services/<int:service_id>/delete_order/<int:order_id>/',
         views.order_delete_view, name='delete_order'),
    path('', views.index, name='index')
    
]
