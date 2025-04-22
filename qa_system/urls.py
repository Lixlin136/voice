from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('chat/', views.chat, name='chat'),
    path('smart_query/', views.smart_query, name='smart_query'),
    # path('user_setting/', views.user_setting, name='user_setting'),
    path('person_setting/', views.person_setting, name='person_setting'),
    # path('user_update/', views.update_profile, name='update_profile'),
    path('set_persona/', views.set_persona, name='set_persona'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    # path('check_email_verification/', views.check_email_verification, name='check_email_verification'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update_avatar/', views.update_avatar, name='update_avatar'),
    path('profile/update_nickname/', views.update_nickname, name='update_nickname'),
    path('profile/update_phone/', views.update_phone, name='update_phone'),
    path('profile/update_email/', views.update_email, name='update_email'),
    path('profile/update_signature/', views.update_signature, name='update_signature')
]