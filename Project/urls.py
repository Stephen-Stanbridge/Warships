from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from warships.views import HomePageView, UserRegistrationView, UserLoginView, DashboardView, UserChangePasswordView, \
    ChallengeView, ChallengeUserView, RejectInvitationView, AcceptInvitationView, GameView, ShootingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view()),
    path('user/register/', UserRegistrationView.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('user/logout', LogoutView.as_view(next_page='/')),
    path('user/dashboard', DashboardView.as_view()),
    path('user/password-change', UserChangePasswordView.as_view()),
    path('user/challenges', ChallengeView.as_view()),
    path('user/challenge/<id>', ChallengeUserView.as_view()),
    path('game/<int:player_b_id>/<int:player_a_id>/reject', RejectInvitationView.as_view()),
    path('game/<int:player_b_id>/<int:player_a_id>/accept', AcceptInvitationView.as_view()),
    path('game/<int:game_id>', GameView.as_view()),
    path('game/<int:game_id>/shoot/<int:shooter>/<int:shot>/<int:row>/<int:col>', ShootingView.as_view())
]
