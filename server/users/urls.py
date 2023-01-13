from django.urls import path

from django.contrib.auth.views import LogoutView

from .views import SignUpView, CustomLoginView

from users import views as users_views

app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile',users_views.profile, name="profile"),
]