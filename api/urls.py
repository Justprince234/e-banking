from django.urls import path
from knox import views as knox_views
from accounts.views import RegisterAPI, LoginAPIView, UserAPI, ContactList, InternaltionalTransferAPIView, LocalTransferAPIView
from accounts import views

urlpatterns = [
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/', UserAPI.as_view(), name='user'),
    path('all-users/', views.all_user_view),
    path('internationaltransferview/', InternaltionalTransferAPIView.as_view()),
    path('localtransferview/', LocalTransferAPIView.as_view()),
    path('historiesview/', views.histories_api_view, name='historiesview'),
    path('contactlist/', ContactList.as_view()),
    path('profileupdate/', views.profiles_api_view),
]