from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from warships.field_creator import create_ships, create_table
from warships.models import Game, Field
from warships.user_service_views import *


class HomePageView(View):
    def get(self, request):
        return render(request, 'index.html')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request):
        active_games = Game.objects.filter(player_a=request.user, is_accepted=True) | \
                       Game.objects.filter(player_b=request.user, is_accepted=True)
        return render(request, 'dashboard.html', {'active_games': active_games})


class ChallengeView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request):
        users = User.objects.all().exclude(id=request.user.id)
        logged_user = request.user
        games_created_by_logged_user_not_accepted = Game.objects.all().filter(player_a=request.user).filter(
            is_accepted=False)
        games_pending_for_logged_user = Game.objects.all().filter(player_b=request.user).filter(is_accepted=False)
        created_by_logged_user_not_accepted = []
        for game in games_created_by_logged_user_not_accepted:
            created_by_logged_user_not_accepted.append(game.player_b)

        logged_user_invited = []
        for game in games_pending_for_logged_user:
            logged_user_invited.append(game.player_a)

        games_accepted = Game.objects.all().filter(player_a=request.user).filter(is_accepted=True) | \
                         Game.objects.all().filter(player_b=request.user).filter(is_accepted=True)
        active_games = []
        for game in games_accepted:
            active_games.append(game.player_a)
            active_games.append(game.player_b)


        dict = {
            'users': users,
            'created_by_logged_user_not_accepted': created_by_logged_user_not_accepted,
            'logged_user_invited': logged_user_invited,
            'logged_user': logged_user,
            'active_games': active_games,
        }
        return render(request, 'challenge.html', dict)


class ChallengeUserView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request, id):
        challenger = request.user
        challenged = User.objects.get(pk=id)
        Game.objects.create(player_a=challenger, player_b=challenged)
        return redirect('/user/challenges')


class RejectInvitationView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request, player_a_id, player_b_id):
        game = Game.objects.filter(player_a_id=player_a_id).filter(player_b_id=player_b_id)
        game.delete()
        return redirect('/user/challenges')


class AcceptInvitationView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request, player_a_id, player_b_id):
        player_a = User.objects.get(pk=player_a_id)
        player_b = User.objects.get(pk=player_b_id)
        game = Game.objects.get(player_a=player_a, player_b=player_b, is_accepted=False)
        game.is_accepted = True
        game.whose_turn = request.user.id
        game.save()
        # Creating empty table
        table = create_table(game.field_size)
        # Creating ships [amount, how long]
        new_ships = [[1, 4], [1, 3], [2, 2], [2, 1]]
        # Making field for challenging user
        Field.objects.create(game=game, owner_of_field=player_a, table=create_ships(new_ships, table))
        table = create_table(game.field_size)
        # Making field for challenged user
        Field.objects.create(game=game, owner_of_field=player_b, table=create_ships(new_ships, table))
        return redirect('/user/challenges')


class GameView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        if game.player_a == request.user:
            enemy_player = game.player_b
        else:
            enemy_player = game.player_a
        enemy_player_field = Field.objects.get(owner_of_field=enemy_player, game=game)
        user_field = Field.objects.get(owner_of_field=request.user, game=game)

        dict = {
            'game': game,
            'enemy_player': enemy_player,
            'enemy_player_field': enemy_player_field,
            'user_field': user_field,
            'field_size': range(game.field_size + 1)
        }
        return render(request, 'game_view.html', dict)


class ShootingView(LoginRequiredMixin, View):
    login_url = '/user/login'
    def get(self, request, game_id, shooter, shot, row, col):
        game = Game.objects.get(pk=game_id)
        enemy_player = User.objects.get(pk=shot)
        if game.whose_turn == shooter:
            shot_field = Field.objects.get(game=game, owner_of_field=enemy_player)
            table = shot_field.table
            hit = table[row][col]
            if hit == 0:
                hit = 2
            elif hit == 1:
                hit = 3
            elif hit == 2 or hit == 3:
                return render(request, 'game_view.html', {'error': 'You have already shot there'})
            table[row][col] = hit
            check = 0
            for row in table:
                for col in row:
                    if col == 1:
                        check += 1
            if check == 0:
                game.delete()
                return HttpResponse("Wygrales gre")

            shot_field.table = table
            shot_field.save()
            game.whose_turn = shot
            game.save()
            return redirect('/game/' + str(game_id))
        else:
            return render(request, 'game_view.html', {'error': 'Not your turn'})
