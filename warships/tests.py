import pytest
from django.contrib.auth.models import User

from warships.models import Game, Field


@pytest.mark.django_db
def test_creating_players(create_players):
    assert len(User.objects.all()) == 2


@pytest.mark.django_db
def test_deleting_players(create_players):
    player = User.objects.get(username='testing_a')
    player.delete()
    assert len(User.objects.all()) == 1
    assert User.objects.get(username='testing_b')


@pytest.mark.django_db
def test_creating_game(create_players):
    player_a = User.objects.get(username='testing_a')
    player_b = User.objects.get(username='testing_b')
    Game.objects.create(player_a=player_a, player_b=player_b)
    assert len(Game.objects.all()) == 1
    assert Game.objects.get(pk=1)


@pytest.mark.django_db
def test_creating_field(create_players):
    player_a = User.objects.get(username='testing_a')
    player_b = User.objects.get(username='testing_b')
    game = Game.objects.create(player_a=player_a, player_b=player_b)
    Field.objects.create(game=game, owner_of_field=player_a)
    assert len(Field.objects.all()) == 1
    assert Field.objects.get(game=game)
