# import_data/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('display_data/', views.display_data, name='display_data'),
    # path('display_graph/', views.display_graph, name='display_graph'),
    path('map/', views.map_view, name='map'),
    path('get_geojson/', views.get_geojson, name='get_geojson'),  # Add this line
    path('get_terminal_details/<int:terminal_id>/', views.get_terminal_details, name='get_terminal_details'),
    

]
