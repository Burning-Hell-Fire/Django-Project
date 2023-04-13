
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
    path('activate/<int:pk>/', views.activate_account, name='activate'),
    path('activate_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('dashboard/image_upload/', views.image_upload, name='img_upload'),
    path('dashboard/image_view/', views.image_view, name='img_view'),
]