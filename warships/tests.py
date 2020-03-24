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
def test_shooting(c, player_a, player_b):
    table_a = create_table(8)
    table_b = create_table(8)
    table_a[2][2] = 1
    table_a[2][3] = 1
    table_b[2][1] = 1
    game = Game.objects.create(player_a=player_a, player_b=player_b, is_accepted=True, whose_turn=player_a.id)
    f1 = Field.objects.create(game=game, owner_of_field=player_a, table=table_a)
    f2 = Field.objects.create(game=game, owner_of_field=player_b, table=table_b)
    game.field_set.set([f1, f2])
    assert len(Game.objects.all()) == 1
    c.force_login(player_a)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_a.id) + '/' + str(player_b.id) + '/3/1')
    get_player_b_table = Field.objects.get(owner_of_field=player_b).table
    assert get_player_b_table[3][1] == 2
    c.logout()
    c.force_login(player_b)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_b.id) + '/' + str(player_a.id) + '/2/2')
    get_player_a_table = Field.objects.get(owner_of_field=player_a).table
    assert get_player_a_table[2][2] == 3
    c.logout()
    c.force_login(player_a)
    c.get('/game/' + str(game.id) + '/shoot/' + str(player_a.id) + '/' + str(player_b.id) + '/2/1')
    assert len(Game.objects.all()) == 0
