from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_view, name='register'),

    path('cafeteria/', views.cafeteria_view, name='cafeteria'),
    path('bus-schedules/', views.bus_schedules_view, name='bus_schedules'),
    path('class-schedules/', views.class_schedules_view, name='class_schedules'),
    path('events/', views.events_view, name='events'),
    path('campus-map/', views.campus_map_view, name='campus_map'),
    path('buildings-json/', views.buildings_json, name='buildings_json'),  # Optional JSON endpoint
]
