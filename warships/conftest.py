import pytest
from django.contrib.auth.models import User
from django.test import Client

from warships.models import Game, Field


@pytest.fixture
def player_a():
    player_a = User.objects.create(username='testing_a', password="testing", email='testa@test.com')
    return player_a


@pytest.fixture
def player_b():
    player_b = User.objects.create(username='testing_b', password="testing", email='testb@test.com')
    return player_b


@pytest.fixture
def c():
    client = Client()
    return client