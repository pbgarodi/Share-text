"""Share_Text URL Configuration

"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from share_txt_sms_web_app import views as share_txt_view



urlpatterns = [
    url(r'^admin/', admin.site.urls),  
    url('register/', share_txt_view.register, name='register'),
    url('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url('show_text/',share_txt_view.show_text,name = 'show_text' ),
    url(r'',share_txt_view.home, name='users-home'),

]
