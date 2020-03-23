import pytest
from django.contrib.auth.models import User

from warships.models import Game, Field


@pytest.mark.django_db
def test_creating_players(player_a):
    assert len(User.objects.all()) == 1


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


@pytest.mark.django_db
def test_registration(c):
    response = c.post('/user/register', {'username': 'testing', 'password1': '#difficult#1', 'password2': '#difficult#1',
                                          'email': 'test@test.com'})
    assert response.status_code == 302
    assert User.objects.get(username='testing')


@pytest.mark.django_db
def test_login(c, player_a):
    response = c.post('/user/login', {'username': 'testing_a', 'password': 'testing'})
    assert response.status_code == 302
    assert response.url == '/user/dashboard'


@pytest.mark.django_db
def test_changing_password(c, player_a):
    c.login(username='testing_a', password='testing')
    response = c.post('/user/password-change', {'old_password': 'testing', 'new_password1': '#difficult#2',
                                                'new_password2': '#difficult#2'})
    assert response.status_code == 302
    assert response.url == '/user/dashboard'
    c.logout()
    assert c.login(username='testing_a', password='#difficult#2')