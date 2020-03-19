import pytest
from django.contrib.auth.models import User

from warships.models import Game, Field


@pytest.mark.django_db
def test_creating_players(player_a):
    assert len(User.objects.all()) == 1


@pytest.mark.django_db
def test_deleting_players(player_a):
    assert len(User.objects.all()) == 1
    player_a.delete()
    assert len(User.objects.all()) == 0


@pytest.mark.django_db
def test_creating_game(player_a, player_b):
    Game.objects.create(player_a=player_a, player_b=player_b)
    assert len(Game.objects.all()) == 1
    assert Game.objects.get(pk=1)


@pytest.mark.django_db
def test_creating_field(player_a, player_b):
    game = Game.objects.create(player_a=player_a, player_b=player_b)
    Field.objects.create(game=game, owner_of_field=player_a)
    assert len(Field.objects.all()) == 1
    assert Field.objects.get(pk=1)


