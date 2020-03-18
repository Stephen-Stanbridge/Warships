import pytest
from django.contrib.auth.models import User

from warships.models import Game


@pytest.fixture
def create_players():
    player_a = User.objects.create(username='testing_a', password="testing", email='testa@test.com')
    player_b = User.objects.create(username='testing_b', password="testing", email='testb@test.com')