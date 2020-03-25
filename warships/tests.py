import pytest
from django.contrib.auth.models import User

from warships.field_creator import create_table
from warships.models import Game, Field


@pytest.mark.django_db
def test_creating_player_model(player_a):
    assert User.objects.get(username='testing_a')


@pytest.mark.django_db
def test_creating_game_model(player_a, player_b):
    Game.objects.create(player_a=player_a, player_b=player_b)
    assert Game.objects.get(pk=1)


@pytest.mark.django_db
def test_creating_field_model(player_a, player_b):
    game = Game.objects.create(player_a=player_a, player_b=player_b)
    Field.objects.create(game=game, owner_of_field=player_a)
    assert Field.objects.get(pk=1)


@pytest.mark.django_db
def test_registration(c):
    response = c.post('/user/register/', {'username': 'testing', 'password1': '#difficult#1', 'password2': '#difficult#1',
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


@pytest.mark.django_db
def test_challenging_another_user(c, player_a, player_b):
    c.force_login(player_a)
    enemy_id = User.objects.get(username='testing_b').id
    response = c.get('/user/challenge/' + str(enemy_id))
    assert response.status_code == 302
    response = c.get('/user/challenges')
    assert b'Pending' in response.content
    c.logout()
    c.force_login(player_b)
    response = c.get('/user/challenges')
    assert b'Accept' in response.content and b'Reject' in response.content
    assert Game.objects.get(player_a=player_a, player_b=player_b, is_accepted=False)


@pytest.mark.django_db
def test_rejecting_invitation(c, player_a, player_b):
    Game.objects.create(player_a=player_a, player_b=player_b, is_accepted=False)
    assert len(Game.objects.all()) == 1
    c.force_login(player_b)
    c.get('/game/{}/{}/reject'.format(player_b.id, player_a.id))
    assert len(Game.objects.all()) == 0


@pytest.mark.django_db
def test_accepting_invitation(c, player_a, player_b):
    Game.objects.create(player_a=player_a, player_b=player_b)
    assert len(Game.objects.all()) == 1
    c.force_login(player_b)
    response = c.get('/game/{}/{}/accept'.format(player_b.id, player_a.id))
    game = Game.objects.all()[0]
    assert response.status_code == 302
    assert game.is_accepted
    assert game.whose_turn == player_b.id
    assert len(game.field_set.all()) == 2


@pytest.mark.django_db
def test_shooting_and_missing(c, create_accepted_game):
    player_a = User.objects.all()[0]
    player_b = User.objects.all()[1]
    game = Game.objects.all()[0]
    c.force_login(player_a)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_a.id) + '/' + str(player_b.id) + '/3/1')
    get_player_b_table = Field.objects.get(owner_of_field=player_b).table
    assert get_player_b_table[3][1] == 2


@pytest.mark.django_db
def test_shooting_and_hitting(c, create_accepted_game):
    player_a = User.objects.all()[0]
    player_b = User.objects.all()[1]
    game = Game.objects.all()[0]
    c.force_login(player_a)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_a.id) + '/' + str(player_b.id) + '/2/2')
    get_player_b_table = Field.objects.get(owner_of_field=player_b).table
    assert get_player_b_table[2][2] == 3


@pytest.mark.django_db
def test_shooting_and_hitting_last_ship(c, create_accepted_game):
    player_a = User.objects.all()[0]
    player_b = User.objects.all()[1]
    game = Game.objects.all()[0]
    game.whose_turn = player_b.id
    game.save()
    c.force_login(player_b)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_b.id) + '/' + str(player_a.id) + '/2/2')
    assert len(Game.objects.all()) == 0


@pytest.mark.django_db
def test_shooting_field_where_it_was_already_shot(c, create_accepted_game):
    player_a = User.objects.all()[0]
    player_b = User.objects.all()[1]
    game = Game.objects.all()[0]
    c.force_login(player_a)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_a.id) + '/' + str(player_b.id) + '/2/1')
    game.whose_turn = player_a.id
    game.save()
    response = c.get('/game/' + str(game.id) + '/shoot/' + str(player_a.id) + '/' + str(player_b.id) + '/2/1')
    assert b'You have already shot there' in response.content
