from django.urls import path
from django.conf.urls import url

from . import views, realibi_views

app_name= "main"
urlpatterns = [
   path('', views.index, name='index'),
    path('login', views.login, name='login'),  
    path('logout', views.logout, name='logout'),  
    path('404', views.not_found, name='not_found'),
    path('register', views.register, name='register'),  
    path('portfolio_edit', views.portfolio_edit, name="portfolio_edit"),
    path('portfolio/<int:id>', views.portfolio_show, name="portfolio_show"),
    path('portfolio/<int:id>/achivements', views.achivements_show, name="portfolio_achivements_show"),
    path('portfolio_achivements', views.portfolio_achivements, name="portfolio_achivements"),
    path('portfolio_add_achivement', views.portfolio_add_achivement, name="portfolio_add_achivement"),
    path('portfolio_requests', views.portfolio_requests, name="portfolio_requests"),
    path('delete_achivement', views.delete_achivement, name="delete_achivement"),
    path('update_avatar', views.update_avatar, name="update_avatar"),
    path('update_social', views.update_social, name="update_social"),
    path('switch_search', views.switch_search, name="switch_search"),
    path('download/(?P<path>.*)$', views.download, name="download"),
    path('employer_profile', realibi_views.employer_profile, name="employer_profile"),
    path('send_request', realibi_views.send_request, name="send_request"),
    
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),    
]