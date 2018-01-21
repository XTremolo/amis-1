from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views as core_views

urlpatterns = [
    url(r'^lib/$', core_views.book_list, name='lib'),
    url(r'^login/$', auth_views.login, {'template_name': 'book/login.html', 
    	}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^liber/(?P<pk>\d+)$', core_views.liber, name='liber'),
    url(r'^home/$', core_views.home, name='home'),
    url(r'^createGroup/$', core_views.createGroup, name='createGroup'),
    url(r'^groupBooks/(?P<pk>\d+)$', core_views.groupBooks, name='groupBooks'),
    url(r'^groupBooks/deleteBookFromGroup/(?P<book_id>\d+)/(?P<group_id>\d+)$', core_views.deleteBookFromGroup, name='deleteBookFromGroup'),
    url(r'^home/deleteGroup/(?P<group_id>\d+)$', core_views.deleteGroup, name='deleteGroup'),
    url(r'^home/editGroup/(?P<group_id>\d+)$', core_views.editGroup, name='editGroup'),
]