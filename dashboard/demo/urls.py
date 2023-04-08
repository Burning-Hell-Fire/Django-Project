
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('dashboard/add_data', views.add_data, name='add_data' ),
    path('dashboard/delete', views.delete, name='delete' ),
    path('dashboard/filter',views.filter_data, name='filter_data'),
    path('dashboard/download', views.download, name='download'),
]
