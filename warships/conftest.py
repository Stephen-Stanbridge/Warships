import pytest
from django.contrib.auth.models import User
from django.test import Client

from warships.field_creator import create_table
from warships.models import Game, Field


@pytest.fixture
def player_a():
    player_a = User.objects.create(username='testing_a', password="testing", email='testa@test.com')
    player_a.set_password('testing')
    player_a.save()
    return player_a


@pytest.fixture
def player_b():
    player_b = User.objects.create(username='testing_b', password="testing", email='testb@test.com')
    player_b.set_password('testing')
    player_b.save()
    return player_b


@pytest.fixture
def c():
    client = Client()
    return client


@pytest.fixture
def create_accepted_game():
    player_a = User.objects.create(username='testing_a', password="testing", email='testa@test.com')
    player_b = User.objects.create(username='testing_b', password="testing", email='testb@test.com')
    table_a = create_table(8)
    table_b = create_table(8)
    table_a[2][2] = 1
    table_b[2][2] = 1
    table_b[2][1] = 1
    game = Game.objects.create(player_a=player_a, player_b=player_b, is_accepted=True, whose_turn=player_a.id)
    f1 = Field.objects.create(game=game, owner_of_field=player_a, table=table_a)
    f2 = Field.objects.create(game=game, owner_of_field=player_b, table=table_b)
    game.field_set.set([f1, f2])